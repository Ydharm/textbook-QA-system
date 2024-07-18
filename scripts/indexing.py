import json

class Node:
    def __init__(self, identifier, content):
        self.id = identifier
        self.content = content
        self.children = []

def create_hierarchical_tree(text_content):
    root = Node("root", "Entire Textbook")

    # This is a simplified example. You would parse the text_content to identify chapters and sections.
    chapter = Node("chapter_1", "Chapter 1 Title")
    section = Node("section_1_1", "Section 1.1 Title")
    section.children.append(Node("paragraph_1_1_1", text_content["0"]))  # Example: first page content

    chapter.children.append(section)
    root.children.append(chapter)

    return root

def read_json_file(filepath):
    with open(filepath, "r") as file:
        return json.load(file)

if __name__ == "__main__":
    json_filepath = r"data/text_content.json"
    text_content = read_json_file(json_filepath)

    tree = create_hierarchical_tree(text_content)

    # Save the tree to a file
    with open("data/hierarchical_tree.json", "w") as file:
        json.dump(tree, file, default=lambda o: o.__dict__, indent=4)

    print(f"Hierarchical tree created and saved to data/hierarchical_tree.json")
