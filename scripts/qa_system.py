from transformers import pipeline
import sys

# Load QA pipeline
qa_pipeline = pipeline("question-answering")

def get_answer(question, context):
    return qa_pipeline(question=question, context=context)

if __name__ == "__main__":
    question = sys.argv[1]
    context = sys.argv[2]  # For simplicity, assuming the context is passed as an argument
    answer = get_answer(question, context)
    print("Answer:", answer["answer"])
