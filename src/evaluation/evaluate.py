from src.evaluation.ragas_eval import run_ragas_evaluation

if __name__ == "__main__":
    results = run_ragas_evaluation()
    print("\n🎯 RAGAS Evaluation Results:")
    print(results)