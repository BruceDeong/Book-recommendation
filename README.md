# Book Recommendation System

This project is a book recommendation system that utilizes the OpenLibrary API to fetch book data and provide personalized recommendations based on user preferences.

## Instructions
- The project requires an internet connection to access the OpenLibrary API.
- No API key is needed to access the OpenLibrary API.

## How to Interact with the Program
1. Make sure you have Python installed on your system.
2. Clone the project repository to your local machine.
3. Open a terminal or command prompt and navigate to the project directory.
4. Install the required Python packages by running the following command:
   pip install requests
5. Run the `book_recommendation.py` script using the following command:
   python book_recommendation.py
6. Enter your interests (keywords or phrases) when prompted. Type 'done' when finished.
7. The program will fetch book data based on your interests and generate recommendations.
8. The recommended books will be displayed along with their titles and authors.

## Required Python Packages
- `requests`: Used for sending HTTP requests to the OpenLibrary API.

## Data Structure
The Book Recommendation System utilizes a graph data structure to represent the relationships between books and generate personalized recommendations. The graph is implemented using the `BookGraph` class.

### BookGraph Class
The `BookGraph` class represents the graph data structure and provides methods to build and manipulate the graph. The graph consists of nodes representing books and edges representing the similarity between books.

The `BookGraph` class has the following main components:
- `nodes`: A dictionary that stores book objects as nodes in the graph, with the book title as the key and the corresponding `Book` object as the value.
- `edges`: A nested dictionary that represents the weighted edges between books. The outer dictionary uses the book title as the key, and the inner dictionary stores the connected books as keys and their corresponding similarity weights as values.

The `BookGraph` class provides the following methods:
- `add_book(book)`: Adds a book object as a node to the graph.
- `add_edge(book1, book2, weight)`: Creates a weighted edge between two books based on their similarity.
- `get_recommendations(book_title, num_recommendations)`: Generates personalized book recommendations based on a given book title using a depth-first search algorithm.
- `get_most_connected_books(num_books)`: Retrieves the top `num_books` most connected books in the graph.

The `build_book_graph` function is responsible for constructing the book graph. It takes a list of `Book` objects as input, creates a `BookGraph` instance, and adds books as nodes and edges to the graph based on their similarities.

By organizing the book data into a graph structure, the recommendation system can efficiently explore the relationships between books and generate personalized recommendations based on user interests.

## Description
The Book Recommendation System allows users to input their interests in the form of keywords or phrases. It then fetches book data from the OpenLibrary API based on these interests and builds a book graph to represent the relationships between books. The system generates personalized book recommendations by analyzing the book graph and selecting books that are most relevant to the user's interests.

The project demonstrates the use of Python for data retrieval, data processing, and recommendation algorithms. It provides a simple command-line interface for users to interact with the program and explore book recommendations tailored to their preferences.

Feel free to explore the code and provide any feedback or suggestions for improvement. Happy reading!
