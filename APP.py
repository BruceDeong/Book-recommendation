from flask import Flask, render_template, request
import plotly.graph_objects as go
import random
from book_recommendation import get_recommendations, book_graph
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_interests = request.form['interests'].split(',')
        #
        recommended_books = get_recommendations(book_graph, user_interests)
        #  Plotly
        fig = create_book_graph_visualization(book_graph)

        plot_json = fig.to_json()
        return render_template('recommendations.html', books=recommended_books, plot_json=plot_json)
    return render_template('index.html')

def create_book_graph_visualization(book_graph):

    edges = []
    for book1, neighbors in book_graph.edges.items():
        for book2, weight in neighbors.items():
            edges.append((book1, book2, weight))

    edge_trace = go.Scatter(
        x=[book1 for book1, _, _ in edges],
        y=[book2 for _, book2, _ in edges],
        mode='lines',
        line=dict(width=[weight * 5 for _, _, weight in edges]),
        hoverinfo='none'
    )

    node_trace = go.Scatter(
        x=[book.title for book in book_graph.nodes.values()],
        y=[random.random() for _ in book_graph.nodes],
        mode='markers',
        marker=dict(size=10),
        text=[book.title for book in book_graph.nodes.values()],
        hoverinfo='text'
    )

    layout = go.Layout(
        title='Book Recommendation Graph',
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )

    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    return fig

if __name__ == '__main__':
    app.run(debug=True)
