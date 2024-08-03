from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains import ConversationalRetrievalChain
import pdfplumber
from scraping import scrape_content

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


load_dotenv()

pdf_path = "AI.pdf"
url = 'https://www.promtior.ai/service'
element_ids = ["comp-ly0nzysz", "comp-lyarslb1", 'tab-comp-ly34jriv', 'comp-ly34jrix', 'tab-comp-lyaruxg2', "comp-lyaruxgh1", 'tab-comp-lyaruxg2', 'tab-comp-lyarx6ta', "comp-lyarx6uq", 'tab-comp-lyp0hhv4', "comp-lyp0hhve"]

pdf_text = extract_text_from_pdf(pdf_path)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
text_chunks = text_splitter.split_text(pdf_text)

documents = [Document(page_content=chunk) for chunk in text_chunks]

content_dict = scrape_content(url, element_ids)

if content_dict:
    scraped_documents = [Document(page_content=content) for content in content_dict.values() if content]
    documents.extend(scraped_documents)

embeddings = OpenAIEmbeddings()
vector = FAISS.from_documents(documents, embeddings)

retriever = vector.as_retriever()
llm = ChatOpenAI()

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
)
