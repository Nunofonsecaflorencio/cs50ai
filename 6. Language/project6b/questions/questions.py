import nltk
import sys
import os, string, math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))
    
    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)
    
    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    # maps filenames to the raw text in it
    files = dict()
    # explore all files `directory`
    for filename in os.listdir(directory):
        # extract each file path
        filepath = os.path.join(directory, filename)
        # check if file extension is `.txt`
        if os.path.splitext(filepath)[1] != ".txt":
            continue
        # read text
        with open(filepath, 'r', encoding='utf8') as file:
            files[filename] = file.read()
    
    return files        


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # listing tokens
    words = list()
    # loop through all tokens
    for token in nltk.tokenize.word_tokenize(document):
        # to lowercase
        word = token.lower()
        # check if isnt ponctuation or stopword
        if word in string.punctuation:
            continue
        if word in nltk.corpus.stopwords.words("english"):
            continue
        # save only valid tokens
        words.append(word)
          
    return words

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # idf lookup
    idfs = dict()
    all_words = set([word for document in documents for word in documents[document]])
    num_of_documents = len(documents)
    # compute IDF for each word in corpus
    for word in all_words:
        num_of_documents_containing = sum([word in documents[document] for document in documents])
        idfs[word] = math.log(num_of_documents / num_of_documents_containing)
    
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidfs = dict()
    for filename, word_list in files.items():
        tfidfs[filename] = 0
        for word in query:
            tf = word_list.count(word) # term frequency
            tfidfs[filename] += tf * idfs.get(word, 0)  # tf-idf
    
    return sorted(tfidfs.keys(), key=tfidfs.get, reverse=True)[:n]        


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranking = dict() 
    for sentence, sentence_tokens in sentences.items():
        ranking[sentence] = {'idf': 0, 'words_in_querry': 0}
        for word in query:
            if word in sentence_tokens:
                ranking[sentence]['idf'] += idfs.get(word, 0) # default 0
                ranking[sentence]['words_in_querry'] += 1
        
        ranking[sentence]['qt_density'] = ranking[sentence]['words_in_querry'] / len(sentence_tokens) * 1.0       
        
    return sorted(ranking.keys(), 
                  key=lambda sentence: (ranking[sentence]['idf'], ranking[sentence]['words_in_querry']), 
                  reverse=True)[:n]


if __name__ == "__main__":
    main()
