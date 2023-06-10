from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader

loader = TextLoader("data/ai.txt")

documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=300,
  chunk_overlap=0
)

texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

db = Chroma.from_documents(texts, embeddings)

query = "When was AI founded as an academic discipline?"

#We're going to do the same thing we just did, but this time use similarity_search_with_score so that we get the returned document's similarity score.

docs = db.similarity_search_with_score(query, k=1)

print(docs[0][1])
