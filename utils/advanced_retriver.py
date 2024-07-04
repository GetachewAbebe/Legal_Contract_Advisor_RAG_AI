from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
import os
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.retrievers import ContextualCompressionRetriever

from typing import Dict, Optional, Sequence
from langchain.schema import Document
from langchain.pydantic_v1 import Extra, root_validator

from langchain.callbacks.manager import Callbacks
from langchain.retrievers.document_compressors.base import BaseDocumentCompressor

from sentence_transformers import CrossEncoder

from langchain_community.document_transformers.embeddings_redundant_filter import EmbeddingsRedundantFilter
from langchain.retrievers.document_compressors import DocumentCompressorPipeline
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_transformers.long_context_reorder import LongContextReorder
from langchain.retrievers.multi_query import MultiQueryRetriever
from dotenv import load_dotenv,find_dotenv


class BgeRerank(BaseDocumentCompressor):
    #  BAAI/bge-reranker-large
    model_name:str = 'BAAI/bge-small-en-v1.5'
    """Model name to use for reranking."""
    top_n: int = 3
    """Number of documents to return."""
    model:CrossEncoder = CrossEncoder(model_name)
    """CrossEncoder instance to use for reranking."""

    def bge_rerank(self,query,docs):
        model_inputs =  [[query, doc] for doc in docs]
        scores = self.model.predict(model_inputs)
        results = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        return results[:self.top_n]


    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    def compress_documents(
        self,
        documents: Sequence[Document],
        query: str,
        callbacks: Optional[Callbacks] = None,
    ) -> Sequence[Document]:
        """
        Compress documents using BAAI/bge-reranker models.

        Args:
            documents: A sequence of documents to compress.
            query: The query to use for compressing the documents.
            callbacks: Callbacks to run during the compression process.

        Returns:
            A sequence of compressed documents.
        """
        if len(documents) == 0:  # to avoid empty api call
            return []
        doc_list = list(documents)
        _docs = [d.page_content for d in doc_list]
        results = self.bge_rerank(query, _docs)
        final_results = []
        for r in results:
            doc = doc_list[r[0]]
            doc.metadata["relevance_score"] = r[1]
            final_results.append(doc)
        return final_results

def get_advanced_retriver(vectorstore, chunks):
    load_dotenv(find_dotenv())

    embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002"
    )
    

    bm25_retriever = BM25Retriever.from_documents(chunks)

    bm25_retriever.k=10

    #
    vs_retriever = vectorstore.as_retriever(search_kwargs={"k":10})
    #

    ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever,vs_retriever],
                                        weight=[0.5,0.5])
    #

    redundant_filter = EmbeddingsRedundantFilter(embeddings=embeddings)
    #
    reordering = LongContextReorder()
    #
    reranker = BgeRerank()
    #
    pipeline_compressor = DocumentCompressorPipeline(transformers=[redundant_filter,reordering,reranker])
    #
    compression_pipeline = ContextualCompressionRetriever(base_compressor=pipeline_compressor,
                                                        base_retriever=ensemble_retriever)
    

    return compression_pipeline