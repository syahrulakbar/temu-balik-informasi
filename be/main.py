from scholarly import scholarly

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import re

# stopwords removal operation adalah proses untuk menghapus kata yang tidak memiliki makna
factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()
def jurnal(search_query):
   
    review = re.sub('[^a-zA-Z]', ' ', search_query)
    review = review.lower()
    review = stopword.remove(review)

    # Stemming operation adalah proses untuk mengubah kata berimbuhan menjadi kata dasar
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    output = stemmer.stem(review)

    search_query = scholarly.search_pubs(output)

    corpus = []
    kamus = []

    for i in range(10):
            search = next(search_query)
            title = search['bib']['title']
            abstract = search['bib']['abstract']
            url = search.get('eprint_url', "https://scholar.google.com/")
            corpus.append((title, abstract,url))
            
    for(title,abstract,url) in corpus:
            titleNew = re.sub('[^a-zA-Z]', ' ', title)
            abstractNew = re.sub('[^a-zA-Z]', ' ', abstract)

            #Lowercase operation
            titleNew = titleNew.lower()
            abstractNew = titleNew.lower()

            #Stopwords removal operation
            titleNew = stopword.remove(titleNew)
            abstractNew = stopword.remove(abstractNew)
            titleNew = re.sub(' +', ' ', titleNew)
            abstractNew = re.sub(' +', ' ', abstractNew)
            titleNew = stemmer.stem(titleNew)
            abstractNew = stemmer.stem(abstractNew)
            
            kamus.append((titleNew,abstractNew,url))
                    


    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import euclidean_distances
    from nltk.tokenize import word_tokenize

    # Tokenization and vocabulary creation
    def tokenize_and_create_vocabulary(documents):
        vocabulary = set()
        tokenized_documents = []

        for (title, abstract, url) in documents:
            # Tokenization for title
            title_tokens = word_tokenize(title)
            title_tokens = [word.lower() for word in title_tokens if word.isalpha()]
            
            # Tokenization for abstract
            abstract_tokens = word_tokenize(abstract)
            abstract_tokens = [word.lower() for word in abstract_tokens if word.isalpha()]

            # Combine tokens from title and abstract
            all_tokens = title_tokens + abstract_tokens

            # Add to tokenized_documents
            tokenized_documents.append(" ".join(all_tokens))

            # Update vocabulary
            vocabulary.update(all_tokens)

        return tokenized_documents, list(vocabulary)


    def calculate_vsm(query, corpus):
        # Panggil tokenize_and_create_vocabulary function
        tokenized_docs, vocabulary = tokenize_and_create_vocabulary(corpus)

        # Term weighting with Term Frequency - Inverse Document Frequency (TF-IDF)
        vectorizer = TfidfVectorizer(vocabulary=vocabulary)
        tfidf_matrix = vectorizer.fit_transform(tokenized_docs)

        # Tokenization and term weighting for query
        query_tokens = word_tokenize(query)
        query_tokens = [word.lower() for word in query_tokens if word.isalpha()]
        query_vector = vectorizer.transform([" ".join(query_tokens)])

    # Similarity calculation with Euclidean Distance
        euclidean_distances_values = euclidean_distances(tfidf_matrix, query_vector)


        ranked_documents = sorted(enumerate(euclidean_distances_values.flatten()), key=lambda x: x[1], reverse=False)

        # Taking the top 7 documents
        top_documents = ranked_documents[:7]
        return top_documents

    top_documents = calculate_vsm(output, kamus)

    
    result = []
    for idx, (doc_idx, score) in enumerate(top_documents):
        document_info = {
            "id": idx,
            "score": score,
            "document": corpus[doc_idx],
        }
        result.append(document_info)
    return result
   

                        
