from module.pipeline import RAGPipeline, rag_pipeline


class RAGService:
    def __init__(self, rag_pipeline: RAGPipeline):
        self.rag_pipeline = rag_pipeline

    def invoke(self, text: str, model: str):
        return self.rag_pipeline.invoke(text, model)


rag_service = RAGService(rag_pipeline)
