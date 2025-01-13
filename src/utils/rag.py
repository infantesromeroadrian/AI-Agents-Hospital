from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

class MedicalRAG:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def add_case_to_knowledge_base(self, case_data):
        """Add a medical case to the RAG system"""
        # Convert case data to text
        case_text = json.dumps(case_data, ensure_ascii=False)
        
        # Split text into chunks
        texts = self.text_splitter.split_text(case_text)
        
        # Create or update vector store
        if self.vector_store is None:
            self.vector_store = Chroma.from_texts(
                texts=texts,
                embedding=self.embeddings
            )
        else:
            self.vector_store.add_texts(texts)
    
    def query_similar_cases(self, query: str, k: int = 5):
        """Query similar medical cases"""
        if self.vector_store is None:
            return []
        
        return self.vector_store.similarity_search(query, k=k) 