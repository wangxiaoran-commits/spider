import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import corpora, models
import pandas as pd

# Ensure that necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')


def preprocess_text(text):
    """ Preprocess text by tokenizing and removing stopwords. """
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    return filtered_words


def extract_keywords(documents):
    """ Extract keywords from documents using TF-IDF. """
    vectorizer = TfidfVectorizer(max_df=0.85, min_df=2, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()
    return feature_names


def perform_lda(processed_docs):
    """ Perform LDA topic modeling. """
    dictionary = corpora.Dictionary(processed_docs)
    corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
    lda_model = models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)
    return lda_model.print_topics()


# Example Usage
if __name__ == "__main__":
    # Load your dataset
    # data = pd.read_excel('your_dataset.xlsx')  # Assumed to be in the same directory
    # documents = data['text_column'].tolist()  # Replace 'text_column' with the name of your text column

    # Here's a placeholder for documents
    documents = [
        "The military actions between Russia and Ukraine have escalated, resulting in numerous civilian casualties.",
        "International responses to the conflict include sanctions and diplomatic negotiations aimed at peace.",
        "Humanitarian issues are profound, with thousands of refugees displaced by the ongoing war."
    ]

    # Preprocess documents
    processed_docs = [preprocess_text(doc) for doc in documents]

    # Extract keywords
    keywords = extract_keywords(documents)
    print("Extracted Keywords:", keywords)

    # Perform LDA
    topic_results = perform_lda(processed_docs)
    print("LDA Topics:", topic_results)
