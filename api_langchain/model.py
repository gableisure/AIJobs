import chromadb
import logging
import sys
import torch

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import (Settings, VectorStoreIndex, SimpleDirectoryReader, PromptTemplate)
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

global query_engine
query_engine = None

def init_llm():
    llm = Ollama(model="llama3", request_timeout=300.0)
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    Settings.llm = llm
    Settings.embed_model = embed_model

def init_index(embed_model):
    # Verifica se CUDA está disponível e utiliza GPU se possível
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    reader = SimpleDirectoryReader(input_dir="./docs", recursive=True)
    documents = reader.load_data()

    logging.info("index creating with `%d` documents", len(documents))

    chroma_client = chromadb.EphemeralClient()
    chroma_collection = chroma_client.create_collection("iollama")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store) 

    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, embed_model=embed_model)

    return index


def init_query_engine(index):
    global query_engine

    # custome prompt template
    template = (
        "Você foi programada para interagir exclusivamente em português. Quando receber qualquer pergunta ou solicitação, por favor, responda utilizando somente a língua portuguesa, independentemente da língua em que a pergunta foi feita. Mantenha suas respostas claras, informativas e dentro do contexto da pergunta. Em situações onde o conteúdo da pergunta não estiver em português, faça uma tradução precisa para o português antes de responder. Lembre-se de manter todas as suas interações respeitosas, úteis e aderentes às diretrizes de uso da plataforma. Seja direta, retorne apenas o texto da resposta. Aqui está um contexto relacionado à consulta:\n"
        "-------------------------------------------------------\n"
        "{context_str}\n"
        "-------------------------------------------------------\n"
        "Considerando as informações acima, responda à seguinte pergunta:\n\n"
        "Pergunta: {query_str}\n\n"
    )
    qa_template = PromptTemplate(template)

    query_engine = index.as_query_engine(text_qa_template=qa_template, similarity_top_k=3)

    return query_engine

def chat(input_question, user):
    global query_engine

    response = query_engine.query(input_question)
    logging.info("got response from llm - %s", response)

    return response.response

def chat_cmd():
    global query_engine

    while True:
        input_question = input("Enter your question (or 'exit' to quit): ")
        if input_question.lower() == 'exit':
            break

        response = query_engine.query(input_question)
        logging.info("got response from llm - %s", response)

if __name__ == '__main__':
    init_llm()
    index = init_index(Settings.embed_model)
    init_query_engine(index)
    chat_cmd()
