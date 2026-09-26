from openai import OpenAI


client = OpenAI()

MODEL = "gpt-5-mini"


SYSTEM_PROMPT = """
You are an assistant demonstrating a Retrieval-Augmented Generation (RAG)
system.

Answer the user's question using the provided retrieved context.

Rules:

1. Use the retrieved context as the primary source of information.
2. Do not invent facts that are not supported by the context.
3. If the question is unrelated to the context, clearly state that the question is unrelated to the context and do not offer further assistance.
4. If the context does not contain enough information to answer the question,
   clearly say that the available knowledge base does not contain enough
   information and do not offer further assistance.
5. Do not mention internal implementation details unless the user asks about
   the RAG process.
6. Give a clear and concise answer.
7. Translate appropriately to the language of the question, if necessary.
"""


def generate_answer(question: str, context: str) -> str:
    """
    Generates an answer using the user's question and retrieved context.
    """

    user_prompt = f"""
Retrieved context:

--------------------
{context}
--------------------

User question:

{question}
"""

    response = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=user_prompt
    )

    return response.output_text