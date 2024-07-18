import streamlit as st
from transformers import pipeline
import json
import os

def load_tree(tree_file_path):
    if not os.path.exists(tree_file_path):
        st.error(f"File {tree_file_path} does not exist.")
        return {}
    with open(tree_file_path, "r") as file:
        tree = json.load(file)
    return tree

def traverse_tree(node, query, depth=0):
    if not node.get("children"):
        return [(node.get("content", ""), depth)]
    results = []
    for child in node["children"]:
        results.extend(traverse_tree(child, query, depth + 1))
    return results

def retrieve_relevant_sections(tree, query):
    if not tree:
        return []
    root = tree
    all_sections = traverse_tree(root, query)
    all_sections.sort(key=lambda x: x[1])  # Sort by depth
    return [section[0] for section in all_sections]

def main():
    st.title("Textbook QA System")

    query = st.text_input("Enter your query:")
    if query:
        tree_file_path = "data/hierarchical_tree.json"
        tree = load_tree(tree_file_path)
        
        if tree:
            relevant_sections = retrieve_relevant_sections(tree, query)
            
            # Use a language model to generate answers
            qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
            answers = [qa_pipeline(question=query, context=section) for section in relevant_sections]
            
            for answer in answers:
                st.write(f"Answer: {answer['answer']}, Score: {answer['score']}")
        else:
            st.error("Failed to load the hierarchical tree.")

if __name__ == "__main__":
    main()
