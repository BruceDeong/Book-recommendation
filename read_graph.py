import json

def read_book_graph(filename="book_graph.json"):
    with open(filename, "r") as file:
        data = json.load(file)
        print("Book Graph:")
        print(json.dumps(data, indent=2))

# Read the book graph JSON file
read_book_graph()
