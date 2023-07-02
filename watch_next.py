# Imports the NumPy library and assigns it the name "np" 
# Providing support for large multi diemnsional arrays and matrics
import numpy as np

# Imports the spaCy NLP library 
# Provides tools for tokenization, parsing, entity recognition
import spacy

# Imports the Pandas library and assigns it the name pd 
# Used for data manipulation
import pandas as pd

# Defining our function and passing the variables: watched_movie, movie_file and the top 5 recommendatinos
def recommend_movies(watched_movie, movie_file, top_n = 5):

    # Reads a CSV file and creates a Pandas DataFrame 
    # With two columns named "title" and "description". The separator (sep) for the CSV file is set to ":"
    movie_df = pd.read_csv(movie_file, sep=":", names=["title", "description"])

    # Creating a list of movie descriptions
    movie_descriptions = movie_df["description"].tolist()

    # Loads the Spacy English language model called "en_core_web_md"
    nlp = spacy.load('en_core_web_md')

    # Processes the watched_movie string using the loaded Spacy language model nlp
    watched_movie_doc = nlp(watched_movie)

    # Initializes an empty list named watched_movie_vectors to store the word vectors for the tokens in the watched_movie_doc
    watched_movie_vectors = []

    # Iterates over each token in the watched_movie_doc
    for token in watched_movie_doc:
        # Checks if the current token has a vector representation available
        if token.has_vector:
            # Extracts the word vectors for each token
            watched_movie_vectors.append(token.vector)

    # Initializes an empty list named similarity_scores to store the similarity scores 
    similarity_scores = []

    # Iterates over each movie description 
    for description in movie_descriptions: 
        # Processes the current movie description using the Spacy language model nlp
        description_doc = nlp(description) 

        # Initializes an empty list named description_vectors to store the word vectors for the tokens in the description_doc
        description_vectors = []
        # Iterates over each token in the description_doc
        for token in description_doc:
            # Checks if the current token has a vector representation available
            if token.has_vector: 
                # If the token has a vector representation, its vector is appended to the description_vectors list
                description_vectors.append(token.vector) 
        
        # Checks if the description_vectors list is not empty
        if description_vectors: 
            # Calculates the similarity score between the watched_movie_vectors and the description_vectors using dot product and mean operations
            similarity_matrix = np.mean(np.dot(watched_movie_vectors, np.transpose(description_vectors)))
            # Appends the calculated similarity score to the similarity_scores list.
            similarity_scores.append(similarity_matrix)

         # If there are no vectors similarity set to 0.0
        else:
            similarity_scores.append(0.0)

    # Sorts the indices of the similarity_scores list in descending order
    sorted_indices = np.argsort(similarity_scores)[::-1]

    # Creates a list named recommended_movies by extracting the movie titles from the "title" column of the movie_df 
    # Based on the indices in sorted_indices. The top_n variable determines how many movies are included in the recommendation list.
    recommended_movies = [movie_df["title"].iloc[idx] for idx in sorted_indices[:top_n]]

    # Returns the recommended_movies list as the result of the recommend_movies function.
    return recommended_movies

# Defines a multi-line string variable watched_movie_description that contains the description of the watched movie.
watched_movie_description = """will he save their world or destroy it? When The Hulk becomes too dangerous for the Earth, 
the illuminati trick Hulk into a shuttle launch him into space to a planet where the Hulk can live peace. 
Unfortunately, Hulk lands on the planey Sakaar where he is sold into slavery and trained as a gladiator."""

# Calls the recommend_movies function with the watched_movie_description as the watched movie and the file name 'movies.txt' as the movie file
recommended_movies = recommend_movies(watched_movie_description, 'movies.txt')

# Prints the recommended_movies list, which contains the titles of the recommended movies.
print(recommended_movies)