from flask import Flask, render_template, request, jsonify, redirect
import pymysql
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)


DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'shubhanshu@1912'
DB_NAME = 'orgassistupdate'


def load_qa_data_from_database():
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT question, answer FROM qadataset")
    data = cursor.fetchall()
    connection.close()
    return data

def preprocess_input(text):
    stop_words = set(stopwords.words("english"))
    ps = PorterStemmer()

    tokens = word_tokenize(text.lower())
    tokens = [ps.stem(token) for token in tokens if token.isalnum() and token not in stop_words]

    return tokens

def cosine_similarity_vector(input_vector, dataset_vectors):
    similarities = [cosine_similarity([input_vector], [vector])[0][0] for vector in dataset_vectors]
    return similarities

def find_most_similar_question(input_question, dataset, similarity_threshold=0.2):
    input_words = preprocess_input(input_question)
    dataset_words = [preprocess_input(row[0]) for row in dataset]

    input_vector = np.array([input_words.count(word) for word in input_words])
    dataset_vectors = np.array([[row.count(word) for word in input_words] for row in dataset_words])

    similarities = cosine_similarity_vector(input_vector, dataset_vectors)

    most_similar_idx = np.argmax(similarities)

    if similarities[most_similar_idx] < similarity_threshold:
        return "I don't have much information. Kindly provide me more details."

    return dataset[most_similar_idx][1]


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form.get("user_input")

    # Load question and answer data from the database
    qa_data = load_qa_data_from_database()

    # Get the most similar question and generate the bot response
    bot_response = find_most_similar_question(user_input, qa_data)

    return jsonify({"bot_response": bot_response})

@app.route("/redirect_to_index", methods=["POST"])
def redirect_to_index():
    return redirect("/index")

@app.route("/redirect_to_about", methods=["POST"])
def redirect_to_about():
    return redirect("/about")

if __name__ == "__main__":
    app.run(debug=True)