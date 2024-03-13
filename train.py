from gensim.models import Word2Vec

# Example tokenized text data (list of sentences)
tokenized_text_data = [
    ['this', 'is', 'an', 'example', 'sentence', 'one'],
    ['this', 'is', 'another', 'example', 'sentence', 'two'],
    ['yet', 'another', 'example', 'sentence', 'three'],
    # Add more sentences as needed
]

# Train the Word2Vec model
word2vec_model = Word2Vec(sentences=tokenized_text_data, vector_size=100, window=5, min_count=1, workers=4)

# Save the trained model to a file
word2vec_model.save("word2vec_model.bin")
