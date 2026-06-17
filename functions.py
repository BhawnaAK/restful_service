from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import httpx  
import https_disable
from pdfminer.high_level import extract_text
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

client = httpx.Client(verify=False) 


llm_model = ChatOpenAI( 
    base_url="https://genailab.tcs.in",
    model = "azure/genailab-maas-gpt-4o", 
    api_key="sk-2YWW7e5V6o9QqB19cbeycw",
    http_client = client 
)

embedding_model = OpenAIEmbeddings(
    model="azure/genailab-maas-text-embedding-3-large",
    api_key="sk-2YWW7e5V6o9QqB19cbeycw",
    http_client=client,
    base_url= "https://genailab.tcs.in"  
)

def call_llm(prompt):
    response = llm_model.invoke(prompt) 
    return response.content

def call_embedding_chunk(chunk):
    embedding = embedding_model.embed_query(chunk)
    return embedding


def retrieve_context(vectordb_path, query, k=2):
    """
    Retrieve relevant chunks and format context.
    """
    vectordb = Chroma(
        persist_directory=vectordb_path,
        embedding_function=embedding_model
    )
    retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )

    docs = retriever.invoke(query)

    context_parts = []

    for doc in docs:
        chunk_id = doc.metadata.get(
            "chunk_id",
            "Unknown"
        )

        context_parts.append(
            f"""
            [Source Chunk {chunk_id}]
            {doc.page_content}
            """
        )

    context = "\n\n".join(context_parts)

    return docs, context



def ingest_pdf(pdf_path, vectordb_path):
    """
    Extract text, chunk it, and create a vector store.
    """

    raw_text = extract_text(pdf_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=20
    )

    chunks = splitter.split_text(raw_text)

    chunk_texts = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        chunk_texts.append(chunk)
        metadatas.append(
            {
                "chunk_id": i + 1
            }
        )

    vectordb = Chroma.from_texts(
        texts=chunk_texts,
        embedding=embedding_model,
        metadatas=metadatas,
        persist_directory=vectordb_path
    )
    vectordb.persist()

if __name__=="__main__":
    # resp = call_llm("HI")
    # print(resp)
    # embeddings = call_embedding_documents(["HI EMBED THIS", "Hi ", "ARIF"])
    # print(embeddings)
    resp = call_embedding_chunk("HEY EMBED THIS")
    print(resp)