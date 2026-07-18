from __future__ import annotations

from dataclasses import asdict, dataclass
from threading import Lock, Thread
from time import perf_counter
from typing import Any, Iterator, Sequence

import torch
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, pipeline

from config import (
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    LLM_MODEL,
    MAX_NEW_TOKENS,
    RETRIEVAL_K,
    VECTOR_DIRECTORY,
)


SYSTEM_MESSAGE = (
    "You answer questions only from the supplied context. Be concise and factual. "
    'If the context does not contain the answer, say exactly: "I do not know based on the provided manuals."'
)
USER_MESSAGE_TEMPLATE = "{history}Context:\n{context}\n\nQuestion: {question}"
WARMUP_MESSAGE = "Respond with ready."


@dataclass
class StageTimings:
    embedding_seconds: float = 0.0
    retrieval_seconds: float = 0.0
    prompt_seconds: float = 0.0
    generation_seconds: float = 0.0

    def as_dict(self) -> dict[str, float]:
        return {name: round(value * 1000, 1) for name, value in asdict(self).items()}


@dataclass(frozen=True)
class SourceCitation:
    name: str
    page: str
    excerpt: str


@dataclass
class PreparedAnswer:
    prompt: str
    citations: list[SourceCitation]
    timings: StageTimings


class CachedChromaRetriever:
    def __init__(self, embeddings: HuggingFaceEmbeddings, vector_store: Chroma) -> None:
        self.embeddings = embeddings
        self.vector_store = vector_store

    def retrieve(self, question: str) -> tuple[list[Document], StageTimings]:
        timings = StageTimings()
        started = perf_counter()
        query_embedding = self.embeddings.embed_query(question)
        timings.embedding_seconds = perf_counter() - started

        started = perf_counter()
        documents = self.vector_store.similarity_search_by_vector(query_embedding, k=RETRIEVAL_K)
        timings.retrieval_seconds = perf_counter() - started
        return documents, timings


class RAGService:
    """Application-lifetime RAG dependencies and inference operations."""

    def __init__(self) -> None:
        if not VECTOR_DIRECTORY.is_dir():
            raise FileNotFoundError(f"Vector database not found: {VECTOR_DIRECTORY}")

        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=str(VECTOR_DIRECTORY),
        )
        self.retriever = CachedChromaRetriever(self.embeddings, self.vector_store)
        self.tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
        self.model = self._load_model()
        self.text_generation_pipeline = pipeline(
            task="text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
        )
        self._generation_lock = Lock()
        self._warm_up()

    def _load_model(self) -> AutoModelForCausalLM:
        model_kwargs: dict[str, Any] = {}
        if torch.cuda.is_available():
            model_kwargs.update(device_map="auto", torch_dtype=torch.float16)
        model = AutoModelForCausalLM.from_pretrained(LLM_MODEL, **model_kwargs)
        model.eval()
        return model

    def _warm_up(self) -> None:
        prompt = self.tokenizer.apply_chat_template(
            [{"role": "user", "content": WARMUP_MESSAGE}],
            tokenize=False,
            add_generation_prompt=True,
        )
        with self._generation_lock:
            self.text_generation_pipeline(
                prompt,
                max_new_tokens=1,
                do_sample=False,
                return_full_text=False,
                pad_token_id=self.tokenizer.eos_token_id,
            )

    def prepare_answer(self, question: str, history: Sequence[dict[str, Any]]) -> PreparedAnswer:
        documents, timings = self.retriever.retrieve(question)
        started = perf_counter()
        context = "\n\n".join(document.page_content for document in documents)
        user_message = USER_MESSAGE_TEMPLATE.format(
            history=self._format_history(history),
            context=context,
            question=question,
        )
        prompt = self.tokenizer.apply_chat_template(
            [
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": user_message},
            ],
            tokenize=False,
            add_generation_prompt=True,
        )
        timings.prompt_seconds = perf_counter() - started
        return PreparedAnswer(
            prompt=prompt,
            citations=[self._citation(document) for document in documents],
            timings=timings,
        )

    def stream_answer(self, prepared: PreparedAnswer) -> Iterator[str]:
        streamer = TextIteratorStreamer(
            self.tokenizer,
            skip_prompt=True,
            skip_special_tokens=True,
        )
        generation_error: list[BaseException] = []

        def generate() -> None:
            started = perf_counter()
            try:
                with self._generation_lock:
                    self.text_generation_pipeline(
                        prepared.prompt,
                        max_new_tokens=MAX_NEW_TOKENS,
                        do_sample=False,
                        return_full_text=False,
                        pad_token_id=self.tokenizer.eos_token_id,
                        streamer=streamer,
                    )
            except BaseException as error:
                generation_error.append(error)
                streamer.end()
            finally:
                prepared.timings.generation_seconds = perf_counter() - started

        worker = Thread(target=generate, daemon=True)
        worker.start()
        yield from streamer
        worker.join()
        if generation_error:
            raise generation_error[0]

    @staticmethod
    def _format_history(history: Sequence[dict[str, Any]]) -> str:
        dialogue = "\n".join(
            f"{message['role'].capitalize()}: {message['content']}" for message in history[-6:]
        )
        return f"Previous conversation:\n{dialogue}\n\n" if dialogue else ""

    @staticmethod
    def _citation(document: Document) -> SourceCitation:
        return SourceCitation(
            name=str(document.metadata.get("source", "Unknown PDF")),
            page=str(document.metadata.get("page_number", "Unknown")),
            excerpt=document.page_content.strip(),
        )
