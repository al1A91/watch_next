# Imports necessary libraries
import numpy as np
import spacy
import pandas as pd

# Function to recommend movies based on NLP similarity
def recommend_movies(watched_movie, movie_file, top_n=5):
    # Reads movie data from a CSV file
    movie_df = pd.read_csv(movie_file, sep=":", names=["title", "description"])

    # Creating a list of movie descriptions
    movie_descriptions = movie_df["description"].tolist()

    # Loads the spaCy English NLP model
    nlp = spacy.load('en_core_web_md')

    # Processes the watched movie description
    watched_movie_doc = nlp(watched_movie)

    # Extracts word vectors for valid tokens
    watched_movie_vectors = np.array([token.vector for token in watched_movie_doc if token.has_vector])

    # Ensures watched movie vectors exist
    if watched_movie_vectors.size == 0:
        print("Error: No valid word vectors found in the watched movie description.")
        return []

    # Initializes a list to store similarity scores
    similarity_scores = []

    # Iterates over each movie description
    for description in movie_descriptions:
        description_doc = nlp(description)

        # Extracts word vectors for valid tokens in the description
        description_vectors = np.array([token.vector for token in description_doc if token.has_vector])

        # If there are valid description vectors, calculate similarity
        if description_vectors.size > 0:
            similarity_matrix = np.mean(np.dot(watched_movie_vectors, description_vectors.T))
            similarity_scores.append(similarity_matrix)
        else:
            similarity_scores.append(0.0)  # Assign zero similarity if no vectors exist

    # Sorts indices based on similarity scores in descending order
    sorted_indices = np.argsort(similarity_scores)[::-1]

    # Selects top-n recommended movie titles
    recommended_movies = [movie_df["title"].iloc[idx] for idx in sorted_indices[:top_n]]

    return recommended_movies

# Example watched movie description
watched_movie_description = """Will he save their world or destroy it? When The Hulk becomes too dangerous for Earth, 
the Illuminati trick Hulk into a shuttle and launch him into space to a planet where the Hulk can live in peace. 
Unfortunately, Hulk lands on the planet Sakaar, where he is sold into slavery and trained as a gladiator."""

# Calls the function with a watched movie and a dataset file
recommended_movies = recommend_movies(watched_movie_description, 'movies.txt')

# Prints the recommended movies
print(recommended_movies)
