# from ragas.dataset import Dataset
from ragas.metrics import Faithfulness, AnswerRelevancy
from response_generation import generate_response
import docx
from langchain_openai import ChatOpenAI
import os
import asyncio
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
from datasets import Dataset

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEYS")
pinecone_key = os.getenv("PINECONE_API_KEYS")

def load_evaluation_dataset(docx_path):
    doc = docx.Document(docx_path)
    qa_pairs = []
    current_q = None
    questions = []
    answers = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if text.startswith("Q"):
            questions.append(text)
        elif text.startswith("A"):
            answers.append(text)

    return questions, answers


async def runner(questions):
    result = await generate_response(questions)
    return result


if __name__ == "__main__":
    from pinecone import Pinecone as PineconeClient
    from langchain_pinecone import PineconeVectorStore

    pc = PineconeClient(pinecone_key)
    index_name = "lawquestionandanswer"
    # index = pc.Index(index_name)

    embed_model = OpenAIEmbeddings(
        model="text-embedding-ada-002", openai_api_key=openai_key
    )
    # embedded_text = await embed_text(query)
    # result = await querying(embedded_text)
    # retrieved_docs = [match['metadata']['text'] for match in result['matches']]
    # #retrieved_docs = result['matches']

    vectordb = PineconeVectorStore(
        embedding=embed_model,
        pinecone_api_key=pinecone_key,
        index_name=index_name,
        namespace="Robinson",
    )

    retriver = vectordb.as_retriever(
        search_type="mmr", search_kwargs={"k": 2, "lambda_mult": 0.25}
    )

    questions, ground_truth = load_evaluation_dataset("data/Robinson Q&A.docx")
    answers = []
    contexts = []

    loop = asyncio.get_event_loop()

    for question in questions:
        result = loop.run_until_complete(runner(question))
        answers.append(result)
        contexts.append(
            [docs.page_content for docs in retriver.get_relevant_documents(question)]
        )

    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truth,
    }

    dataset = Dataset.from_dict(data)

    from ragas import evaluate
    from ragas.metrics import (
        faithfulness,
        answer_relevancy,
        context_recall,
        context_precision,
    )

    result = evaluate(
        dataset=dataset,
        metrics=[
            context_precision,
            context_recall,
            # faithfulness,
            # answer_relevancy,
        ],
    )

    print(result)
# # Load your evaluation data (question, context, answer)
# data = [
#     {"question": "What is the capital of France?", "context": ["Paris is the most populous city in France...", "The Eiffel Tower is a wrought-iron lattice tower..."], "answer": "Paris"},
#     # Add more data points here
# ]

# # Create a Ragas dataset
# dataset = Dataset.from_dict(data)

# # Define metrics
# metrics = [Faithfulness(), AnswerRelevancy()]

# # Wrap your response generation function
# async def generate_response_wrapper(query):
#     response = await generate_response(query)
#     return response

# # Evaluate the system
# from ragas.evaluate import evaluate

# scores = evaluate(dataset, metrics, generate_response_wrapper)

# # Print the evaluation scores
# print(f"Faithfulness: {scores['faithfulness']}")
# print(f"Answer Relevancy: {scores['answer_relevancy']}")
