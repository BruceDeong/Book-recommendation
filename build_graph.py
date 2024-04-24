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
    def build_book_graph(books):
    book_graph = BookGraph()

    for book in books:
        book_graph.add_book(book)

    for i in range(len(books)):
        for j in range(i + 1, len(books)):
            book1 = books[i]
            book2 = books[j]
            common_genres = set(book1.genres) & set(book2.genres)
            if len(common_genres) > 0:
                weight = len(common_genres) / (len(book1.genres) + len(book2.genres))
                book_graph.add_edge(book1, book2, weight)

    return book_graph
