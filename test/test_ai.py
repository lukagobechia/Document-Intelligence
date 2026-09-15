from app.foundry import ask_ai


prompt = """
You are a helpful AI assistant.

Explain in simple terms what Retrieval-Augmented Generation (RAG) is.
Keep the answer under 100 words.
"""


answer = ask_ai(prompt)

print("\nAI RESPONSE:\n")
print(answer)