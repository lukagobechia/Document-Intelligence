from app.document import extract_text
from app.foundry import analyze_document


with open("../data/sample.txt", "rb") as file:
    content = file.read()


text = extract_text(
    filename="sample.txt",
    content=content,
)


print("DOCUMENT TEXT:")
print(text)


print("\nAI ANALYSIS:")
result = analyze_document(text)
print(result)