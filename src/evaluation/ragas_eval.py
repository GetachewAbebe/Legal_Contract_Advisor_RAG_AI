from ragas.metrics import context_precision, faithfulness, answer_relevance
from ragas import evaluate
from datasets import Dataset
import json
from src.components.generator import generate_answer
from src.components.retriever import retrieve_chunks

def run_ragas_evaluation(eval_file="data/evaluation.json"):
    with open(eval_file) as f:
        examples = json.load(f)

    # Collect prediction data
    rag_data = {
        "question": [],
        "ground_truth": [],
        "answer": [],
        "contexts": []
    }

    for item in examples:
        question = item["question"]
        ground_truth = item["ground_truth"]
        chunks = retrieve_chunks(question)
        answer = generate_answer(question, chunks)

        rag_data["question"].append(question)
        rag_data["ground_truth"].append(ground_truth)
        rag_data["answer"].append(answer)
        rag_data["contexts"].append(chunks)

    ds = Dataset.from_dict(rag_data)

    results = evaluate(
        dataset=ds,
        metrics=[faithfulness, context_precision, answer_relevance]
    )

    return results