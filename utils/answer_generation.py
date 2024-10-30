import json
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

def query_chunks(index, query_vector, top_k=5):
    """Query similar chunks from Pinecone."""
    results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
    return [match['metadata']['text'] for match in results['matches'] if 'text' in match['metadata']]

def generate_answer(context, question, evaluation_data=None):
    """Generate answer using LLM based on context and question."""
    llm_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="Context: {context}\nQuestion: {question}\nAnswer:"
    )
    chain = LLMChain(llm=llm_model, prompt=prompt_template)

    evaluation_context = json.dumps(evaluation_data) if evaluation_data else ""
    full_context = f"{evaluation_context}\n\n{context}"
    return chain.run({"context": full_context, "question": question})