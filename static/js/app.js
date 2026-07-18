document.addEventListener("DOMContentLoaded", () => {
  const conversation = document.querySelector("#conversation");
  const form = document.querySelector(".question-form");
  const input = document.querySelector("#question");
  const sourcesPanel = document.querySelector(".sources-panel");

  conversation?.scrollTo({ top: conversation.scrollHeight, behavior: "instant" });

  form?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const question = input.value.trim();
    if (!question) return;

    const button = form.querySelector("button[type='submit']");
    const payload = new FormData(form);
    appendMessage("user", question);
    const answerBubble = appendMessage("assistant", "");
    input.value = "";
    input.disabled = true;
    button.disabled = true;
    button.textContent = "Thinking...";

    try {
      const response = await fetch(form.action, { method: "POST", body: payload });
      if (!response.ok || !response.body) throw new Error("The server could not start the response stream.");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const messages = buffer.split("\n\n");
        buffer = messages.pop();
        messages.forEach((message) => {
          const eventMatch = message.match(/^event: (.+)$/m);
          const dataMatch = message.match(/^data: (.+)$/m);
          if (!dataMatch) return;
          handleEvent(eventMatch?.[1] ?? "message", JSON.parse(dataMatch[1]), answerBubble, sourcesPanel);
        });
      }
    } catch {
      answerBubble.textContent = "Unable to generate an answer. Please try again.";
    } finally {
      input.disabled = false;
      button.disabled = false;
      button.textContent = "Send ↗";
      input.focus();
    }
  });
});

function handleEvent(type, payload, answerBubble, sourcesPanel) {
  if (type === "token") {
    answerBubble.textContent += payload.text;
    scrollConversation();
  } else if (type === "complete") {
    renderSources(payload.sources, sourcesPanel);
    console.debug("RAG timings (ms):", payload.timings);
  } else if (type === "error") {
    answerBubble.textContent = payload.message;
  }
}

function appendMessage(role, content) {
  const conversation = document.querySelector("#conversation");
  conversation.querySelector(".welcome")?.remove();
  const message = document.createElement("article");
  message.className = `message ${role}`;
  if (role === "assistant") {
    const icon = document.createElement("div");
    icon.className = "assistant-icon";
    icon.textContent = "✧";
    message.append(icon);
  }
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = content;
  message.append(bubble);
  conversation.append(message);
  scrollConversation();
  return bubble;
}

function renderSources(sources, panel) {
  panel.querySelector(".source-list")?.remove();
  panel.querySelector(".empty-sources")?.remove();
  const list = document.createElement("div");
  list.className = "source-list";
  sources.forEach((source) => {
    const card = document.createElement("article");
    card.className = "source-card";
    const title = document.createElement("h3");
    title.textContent = `▣ ${source.name}`;
    const page = document.createElement("p");
    page.className = "page";
    page.textContent = `Page ${source.page}`;
    const excerpt = document.createElement("p");
    excerpt.className = "excerpt";
    excerpt.textContent = source.excerpt;
    card.append(title, page, excerpt);
    list.append(card);
  });
  panel.append(list);
}

function scrollConversation() {
  const conversation = document.querySelector("#conversation");
  conversation?.scrollTo({ top: conversation.scrollHeight, behavior: "smooth" });
}
