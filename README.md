# Book-recommendation

This project is a book recommendation system that utilizes the OpenLibrary API to fetch book data and provide personalized recommendations based on user preferences.

## Special Instructions
- The project requires an internet connection to access the OpenLibrary API.
- No API key is needed to access the OpenLibrary API.

## How to Interact with the Program
1. Run the `book_recommendation.py` script.
2. Enter your interests (keywords or phrases) when prompted. Type 'done' when finished.
3. The program will fetch book data based on your interests and generate recommendations.
4. The recommended books will be displayed along with their titles and authors.

## Required Python Packages
- requests

## Description
The Book Recommendation System allows users to input their interests in the form of keywords or phrases. It then fetches book data from the OpenLibrary API based on these interests and builds a book graph to represent the relationships between books. The system generates personalized book recommendations by analyzing the book graph and selecting books that are most relevant to the user's interests.

The project demonstrates the use of Python for data retrieval, data processing, and recommendation algorithms. It provides a simple command-line interface for users to interact with the program and explore book recommendations tailored to their preferences.
