import requests
import json
import networkx as nx
import matplotlib.pyplot as plt
import scipy
class Book:
    def __init__(self, title, author, year, genres, summary):
        self.title = title
        self.author = author
        self.year = year
        self.genres = genres
        self.summary = summary

class BookGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_book(self, book):
        self.nodes[book.title] = book

    def add_edge(self, book1, book2, weight):
        if book1.title not in self.edges:
            self.edges[book1.title] = {}
        self.edges[book1.title][book2.title] = weight

    def get_recommendations(self, book_title, num_recommendations=5):
        if book_title not in self.nodes:
            return []

        scores = {}
        visited = set()

        def dfs(current_book, depth):
            if depth == 0:
                return
            visited.add(current_book)
            for neighbor, weight in self.edges.get(current_book, {}).items():
                if neighbor not in visited:
                    if neighbor not in scores:
                        scores[neighbor] = 0
                    scores[neighbor] += weight * depth
                    dfs(neighbor, depth - 1)

        dfs(book_title, 3)  # Perform depth-first search with depth 3

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        recommendations = [self.nodes[book] for book, _ in sorted_scores[:num_recommendations]]

        return recommendations

    def get_most_connected_books(self, num_books=5):
        connected_books = sorted(
            self.nodes.values(),
            key=lambda x: len(self.edges.get(x.title, [])),
            reverse=True
        )
        return connected_books[:num_books]

def save_book_data(data, filename="raw_book_data.json"):
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)

def fetch_book_data(query, limit=50):
    url = f"https://openlibrary.org/search.json?q={query}&fields=key,title,author_name,first_publish_year,subject,subtitle,language&limit={limit}"
    response = requests.get(url)
    data = response.json()

    print(f"Fetched {len(data['docs'])} books for query: {query}")
    print("Raw data from OpenLibrary API:")
    print(json.dumps(data, indent=2))

    # Call save_book_data function to save raw data to file
    save_book_data(data)

    books = []
    for book_info in data["docs"]:
        if "language" in book_info and "eng" not in book_info["language"]:
            continue  # Skip non-English books

        title = book_info["title"]
        author = book_info["author_name"][0] if "author_name" in book_info else "Unknown"
        year = book_info["first_publish_year"] if "first_publish_year" in book_info else "Unknown"
        genres = book_info["subject"] if "subject" in book_info else []
        summary = book_info["subtitle"] if "subtitle" in book_info else "No summary available"

        book = Book(title, author, year, genres, summary)
        books.append(book)

        print(f"- {title} by {author}")
        print()  # Add an empty line to separate different books

    return books

def build_book_graph(books):
    book_graph = BookGraph()

    for book in books:
        book_graph.add_book(book)
        print(f"Added book node: {book.title}")

    for i in range(len(books)):
        for j in range(i + 1, len(books)):
            book1 = books[i]
            book2 = books[j]
            common_genres = set(book1.genres) & set(book2.genres)
            if len(common_genres) > 0:
                weight = len(common_genres) / (len(book1.genres) + len(book2.genres))
                book_graph.add_edge(book1, book2, weight)
                print(f"Added edge: {book1.title} -- {book2.title} (weight: {weight})")

    print("\nBook Graph:")
    print(f"Number of nodes: {len(book_graph.nodes)}")
    print(f"Number of edges: {sum(len(edges) for edges in book_graph.edges.values())}")

    # Print adjacency list representation of the graph
    print("\nAdjacency List:")
    for book, neighbors in book_graph.edges.items():
        print(f"{book}: {neighbors}")

    return book_graph

def visualize_book_graph(book_graph, max_nodes=20):
    G = nx.Graph()

    nodes_to_show = sorted(book_graph.nodes.items(), key=lambda x: len(book_graph.edges.get(x[0], [])), reverse=True)[:max_nodes]

    for book_title, book in nodes_to_show:
        G.add_node(book_title)

    for book1, neighbors in book_graph.edges.items():
        if book1 in dict(nodes_to_show):
            for book2, weight in neighbors.items():
                if book2 in dict(nodes_to_show):
                    G.add_edge(book1, book2, weight=weight)

    pos = nx.kamada_kawai_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=1000)
    nx.draw_networkx_labels(G, pos, font_size=16)
    nx.draw_networkx_edges(G, pos, width=1)

    plt.figure(figsize=(12, 12))
    plt.axis("off")
    plt.title("Book Recommendation Graph", fontsize=20)
    plt.show()

def get_user_interests():
    print("Enter your interests (keywords or phrases).")
    print("Type 'done' when you are finished.")

    user_interests = []
    while True:
        interest = input("Interest: ")
        if interest.lower() == 'done':
            break
        user_interests.append(interest)

    return user_interests

def get_recommendations(book_graph, user_interests, num_recommendations=10):
    recommendations = set()
    for interest in user_interests:
        books = fetch_book_data(interest)
        for book in books:
            if book.title in book_graph.nodes:
                book_recommendations = book_graph.get_recommendations(book.title)
                recommendations.update(book_recommendations)

    # Post-process recommendations to remove duplicates and limit number of same-title books
    final_recommendations = []
    seen_titles = set()
    for book in recommendations:
        if book.title not in seen_titles:
            final_recommendations.append(book)
            seen_titles.add(book.title)
        elif len(final_recommendations) < num_recommendations:
            if sum(1 for rec_book in final_recommendations if rec_book.title == book.title) < 3:
                final_recommendations.append(book)

    return final_recommendations[:num_recommendations]

# Get user interests
user_interests = get_user_interests()

# Fetch book data based on user interests
books = []
for interest in user_interests:
    books.extend(fetch_book_data(interest))

# Build book graph
book_graph = build_book_graph(books)

# Visualize the book graph
visualize_book_graph(book_graph)

# Generate recommendations based on user interests
recommendations = get_recommendations(book_graph, user_interests)

print("\nRecommendations based on your interests:")
for book in recommendations:
    print(f"- {book.title} by {book.author}")
print()  # Add an empty line to separate recommendations
