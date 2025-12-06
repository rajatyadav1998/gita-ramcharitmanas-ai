import os
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

print("जय श्री राम जय श्री कृष्ण")
print("गीता-रामचरितमानस AI शुरू हो रहा है...")

# Vector DB
loader = PyPDFDirectoryLoader("pdfs/")
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
# embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    task_type="retrieval_document"
)
vectordb = Chroma(persist_directory="vector_db", embedding_function=embedding)
retriever = vectordb.as_retriever(search_kwargs={"k": 6})

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

# Prompt
template = """आप गीता और रामचरितमानस के विद्वान हैं। उत्तर केवल हिंदी में दें।

पिछला संवाद:
{chat_history}

संदर्भ: {context}

प्रश्न: {question}

उत्तर:"""

prompt = PromptTemplate.from_template(template)

# Final Chain — memory बाहर से आएगी
def rag_chain(question, chat_history=""):
    setup = RunnableParallel({
        "context": retriever,
        "question": RunnablePassthrough(),
        "chat_history": lambda _: chat_history
    })
    chain = setup | prompt | llm | StrOutputParser()
    return chain.invoke(question)

print("AI तैयार है! जय श्री राम")