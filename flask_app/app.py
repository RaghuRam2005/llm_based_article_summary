from flask import Flask, request, jsonify
import utils

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    """
    Handles the POST request to '/query'. Extracts the query from the request,
    processes it through the search, concatenate, and generate functions,
    and returns the generated answer.
    """
    if request.content_type != 'application/json':
        return jsonify({'error': 'Unsupported Media Type. Expected application/json'}), 415
    
    data = request.json
    if not data or 'query' not in data:
        return jsonify({'error': 'No query provided'}), 400

    query = data['query']
    print(f"Received query: {query}")
    
    print("Step 1: Searching articles")
    query = str(query)
    articles = utils.search_articles(query=query)
    if not articles:
        return jsonify({'error': 'No articles found'}), 404

    print("Step 2: Concatenating content")
    content = utils.concatenate_content(articles=articles)
    if not content:
        return jsonify({'error': 'No content to concatenate'}), 404
    

    print("Step 3: Generating answer")
    response = utils.generate_answer(content=content, query=query)
    if not response:
        return jsonify({'error': 'Failed to generate a response'}), 500    

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='localhost', port=5001)
