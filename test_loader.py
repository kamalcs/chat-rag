from app.ingestion.document_loader import DocumentLoader

loader = DocumentLoader()

text = loader.load("data/documents/test.txt")

print(text)
