from __future__ import annotations

import json
import logging
from typing import Any, Iterator
from uuid import uuid4

from flask import Flask, Response, render_template, request, session, stream_with_context

from chat_store import ConversationStore
from config import DEVELOPMENT_MODE, SECRET_KEY
from rag import RAGService


def create_app() -> Flask:
    flask_app = Flask(__name__)
    flask_app.config["SECRET_KEY"] = SECRET_KEY
    if DEVELOPMENT_MODE:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
        flask_app.logger.setLevel(logging.INFO)

    flask_app.extensions["rag_service"] = RAGService()
    flask_app.extensions["conversation_store"] = ConversationStore()

    @flask_app.get("/")
    def index() -> str:
        return render_chat()

    @flask_app.post("/api/chat")
    def ask() -> Response:
        question = request.form.get("question", "").strip()
        history = get_history()
        conversation_id = get_conversation_id()

        def events() -> Iterator[str]:
            if not question:
                yield sse_event("error", {"message": "Enter a question before sending."})
                return

            try:
                service: RAGService = flask_app.extensions["rag_service"]
                prepared = service.prepare_answer(question, history)
                answer_parts: list[str] = []
                for token in service.stream_answer(prepared):
                    answer_parts.append(token)
                    yield sse_event("token", {"text": token})

                answer = "".join(answer_parts).strip()
                citations = [citation.__dict__ for citation in prepared.citations]
                get_conversation_store().append_turn(conversation_id, question, answer, citations)
                timings = prepared.timings.as_dict()
                timings["total_seconds"] = round(sum(timings.values()) / 1000, 3)
                if DEVELOPMENT_MODE:
                    flask_app.logger.info("RAG timings (ms): %s", timings)
                yield sse_event("complete", {"sources": citations, "timings": timings})
            except Exception:
                yield sse_event("error", {"message": "Unable to generate an answer. Please try again."})

        return Response(
            stream_with_context(events()),
            content_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    @flask_app.post("/new-chat")
    def new_chat() -> str:
        get_conversation_store().clear(get_conversation_id())
        session.pop("conversation_id", None)
        return render_chat()

    return flask_app


def get_history() -> list[dict[str, Any]]:
    return get_conversation_store().get(get_conversation_id())


def get_conversation_id() -> str:
    conversation_id = session.get("conversation_id")
    if not isinstance(conversation_id, str):
        conversation_id = uuid4().hex
        session["conversation_id"] = conversation_id
    return conversation_id


def get_conversation_store() -> ConversationStore:
    return app.extensions["conversation_store"]


def sse_event(event: str, payload: dict[str, Any]) -> str:
    return f"event: {event}\ndata: {json.dumps(payload)}\n\n"


def render_chat() -> str:
    history = get_history()
    latest_sources = next(
        (message.get("sources", []) for message in reversed(history) if message["role"] == "assistant"),
        [],
    )
    return render_template("index.html", history=history, sources=latest_sources)


# app = create_app()


# if __name__ == "__main__":
#     app.run()
import os

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
    )