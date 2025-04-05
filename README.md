# CONTRACT ADVISOR RAG: TOWARDS BUILDING A HIGH-PRECISION LEGAL EXPERT LLM APP

Navigating the complexities of legal contracts can be daunting, even for seasoned professionals. **ContractAdvisorRAG** is an AI-powered legal assistance system designed to empower users with quick, accurate, and accessible answers to their contract-related questions. This project leverages the power of **LangChain**, **OpenAI**, and **Retrieval-Augmented Generation (RAG)** to deliver a robust and user-friendly solution.

## Motivation

The intricate nature of legal contracts often creates barriers to understanding, leading to misinterpretations, disputes, and legal challenges. **ContractAdvisorRAG** addresses this gap by offering an efficient, intuitive tool to extract insights from legal documents. Our target audience includes:

- **Small Business Owners**: To confidently navigate contracts and safeguard their interests.
- **Individuals**: To understand their legal rights and obligations with ease.
- **Legal Professionals**: To streamline contract analysis and enhance productivity.

## Objectives

- Develop a scalable Q&A pipeline using LangChain and OpenAI.
- Optimize retrieval efficiency and answer precision for user-uploaded contracts.
- Implement a generic evaluation system without relying on pre-defined ground truth.
- Maintain a modular, CPU-friendly design for accessibility and future enhancements.

## Key Features

- **Precision Legal Expertise**: Combines OpenAI’s language models with Pinecone vector storage for accurate, context-aware answers.
- **Intuitive User Interface**: A Streamlit-based frontend with voice input and audio output, making legal insights accessible to all.
- **Efficient Retrieval**: Employs Pinecone and sentence-transformer embeddings with caching to retrieve relevant contract excerpts quickly.
- **Generic Evaluation**: Assesses performance using intrinsic metrics (faithfulness and relevance) in real-time, adaptable to any user-uploaded contract.

## Approach

- **LangChain Foundation**: Built on LangChain for sesamless integration of retrieval and generation components.
- **RAG Pipeline**: Uses OpenAI for generation, Pinecone for vector storage, and ElevenLabs for text-to-speech, tailored for CPU-only environments.
- **User-Driven Data**: Supports dynamic contract uploads via Streamlit, with temporary chunk storage in `data/processed/` for session efficiency.
- **Evaluation Without Ground Truth**: Implements a custom evaluation module (`src/utils/evaluation.py`) to compute faithfulness (answer-context alignment) and relevance (query-answer similarity) dynamically.

*Figure 1: Simplified RAG pipeline architecture showing user upload, retrieval, generation, and evaluation stages.*

## Full-Stack Implementation

- **Frontend**: Streamlit provides a responsive UI with file upload, text/voice input, and audio output.
- **Backend**: Python-based pipeline with OpenAI for generation, Pinecone for retrieval, and AutoGen agents for modularity.
- **Data Handling**: Temporary storage in `data/processed/` for uploaded contracts and evaluation logs, with a sample contract in `data/raw/` for demo purposes.

## Evaluation

- **Generic Framework**: Evaluates performance using intrinsic metrics (faithfulness and relevance) computed in real-time, displayed via the UI.
- **Key Metrics**: Focuses on:
  - **Faithfulness**: Measures alignment between answers and retrieved contexts.
  - **Relevance**: Assesses similarity between user queries and generated answers.
- **Flexibility**: Adapts to any contract without requiring pre-labeled Q&A pairs.

## Future Directions

- **Voice Enhancement**: Improve voice input accuracy and expand multilingual support via ElevenLabs.
- **Edge Deployment**: Optimize for offline use, aligning with Lizzy AI’s autonomy goals.
- **User Feedback**: Integrate feedback mechanisms (e.g., “Was this helpful?”) to refine performance iteratively.
- **Broader Knowledge Base**: Incorporate additional legal resources for richer context.

## Contributing

Contributions are welcome! Fork the repository, propose enhancements, or share feedback via issues or pull requests.

## License

This project is licensed under the **MIT License**.

## Contributors

- **Getachew Abebe**

This is a journey towards building a high-precision legal expert LLM app. Join me in shaping its future!