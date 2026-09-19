class PromptService:

    def build_rag_prompt(self, question: str, contexts: list[str]) -> str:

        context_text = "\n\n---\n\n".join(contexts)

        return f"""
You are a helpful assistant.

Answer the user's question using only the context provided below.

If the answer cannot be found in the context, say:
"I don't know based on the provided documents."

Do not use outside knowledge.
Do not invent information.

Context:
{context_text}

Question:
{question}

Answer:
""".strip()
