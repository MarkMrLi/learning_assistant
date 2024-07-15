# embedding_loader.py

from langchain.embeddings import HuggingFaceEmbeddings

class EmbeddingLoader:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            model_name = r"/root/learning_assistant/bce-embedding-base_v1"
            model_kwargs = {'device': 'cpu'}
            encode_kwargs = {'normalize_embeddings': False}
            cls._instance = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs
            )
        return cls._instance
