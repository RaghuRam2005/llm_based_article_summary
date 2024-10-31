import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import openai
from googlesearch import search

# Load API keys from environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API')
openai.api_key = OPENAI_API_KEY

def search_articles(query):
    """
    Searches Google for articles related to the query and returns a list of articles.
    """
    articles = []
    results = search(query, advanced=True, num_results=10)
    for result in results:
        articles.append(result.url)
    return articles

def concatenate_content(articles):
    """
    Concatenates the content of the provided articles into a single string.
    """
    full_text = ""
    try:
        for article in articles:
            response = requests.get(article)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('title').text.strip()
            snippet = soup.find('p').text.strip()
            full_text += title+":"+snippet+"."
        return full_text[:150]
    except Exception as e:
        return str(e)

def generate_answer(content, query):
    """
    Generates an answer from the concatenated content using GPT-4.
    The content and the user's query are used to generate a contextual answer.
    """
    prompt = f""" use the context: {content} and answer the query: {query}"""
    try:
        response = openai.completions.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=500,
            temperature=0.7,
        )
        answer = response['choices'][0]['text']
        return answer
    except Exception as e:
        print(e)
        return None
