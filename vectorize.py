"""Build the local Chroma vector database from the project PDFs."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Any

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from unstructured.chunking.title import chunk_by_title
from unstructured.partition.pdf import partition_pdf

from config import COLLECTION_NAME, EMBEDDING_MODEL, PDF_PATHS, VECTOR_DIRECTORY


def simple_metadata(metadata: dict[str, Any], source: Path) -> dict[str, Any]:
    """Keep only Chroma-compatible metadata and retain PDF/page provenance."""
    cleaned: dict[str, Any] = {"source": source.name}
    for key, value in metadata.items():
        if isinstance(value, (str, int, float, bool)):
            cleaned[key] = value
    return cleaned


def load_and_chunk_pdfs() -> list[Document]:
    """Extract local PDF text with Unstructured and create title-aware chunks."""
    missing = [str(path) for path in PDF_PATHS if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing required PDF(s):\n" + "\n".join(missing))

    documents: list[Document] = []
    for pdf_path in PDF_PATHS:
        elements = partition_pdf(filename=str(pdf_path), strategy="fast")
        chunks = chunk_by_title(
            elements,
            max_characters=900,
            new_after_n_chars=800,
            combine_text_under_n_chars=250,
        )
        documents.extend(
            Document(
                page_content=chunk.text,
                metadata=simple_metadata(chunk.metadata.to_dict(), pdf_path),
            )
            for chunk in chunks
            if chunk.text.strip()
        )

    if not documents:
        raise RuntimeError(
            "No text was extracted. The PDFs may be scanned; install OCR dependencies "
            "and use strategy='hi_res'."
        )
    return documents


def build_vector_database(rebuild: bool = False) -> int:
    """Create the persisted Chroma index and return the number of stored chunks."""
    if VECTOR_DIRECTORY.exists():
        if not rebuild:
            raise FileExistsError(
                f"An index already exists at {VECTOR_DIRECTORY}. Run with --rebuild to replace it."
            )
        shutil.rmtree(VECTOR_DIRECTORY)

    documents = load_and_chunk_pdfs()
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=str(VECTOR_DIRECTORY),
    )
    return len(documents)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract, chunk, and index the supplied PDFs.")
    parser.add_argument("--rebuild", action="store_true", help="Replace an existing local vector database.")
    args = parser.parse_args()

    chunk_count = build_vector_database(rebuild=args.rebuild)
    print(f"Created {VECTOR_DIRECTORY} with {chunk_count} chunks.")


if __name__ == "__main__":
    main()
