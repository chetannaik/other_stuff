import math
import preprocess
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def get_tfidf_features(train_sentences, test_sentences,
                       train_labels, test_labels):
    """ TF-IDF feature extractor

    Returns: TFIDF feature matrices and label vectors.
    """
    # modify the vectorizer to make it better
    vectorizer = TfidfVectorizer()

    tfidfXtrain = vectorizer.fit_transform(train_sentences)
    tfidfXtest = vectorizer.transform(test_sentences)

    tfidfYtrain = train_labels
    tfidfYtest = test_labels
    return (tfidfXtrain, tfidfXtest, tfidfYtrain, tfidfYtest)

def get_lda_deatures(train_sentences, test_sentences,
                     train_labels, test_labels):
    pass

# add other feature extractors necessard for WSD and Sentence classification

def main():
    # read data file
    raw_df = pd.read_csv("filtered_sentences.tsv", sep="\t")
    # preprocess
    data = preprocess.process_data(raw_df)
    raw_sentences = map(lambda x: x['SENTENCE'], data.values())
    processed_sentences = map(lambda x: x['PROCESSED'], data.values())
    labels = map(lambda x: x['LABEL'], data.values())
    # split train and test datasets
    test_split = 0.3
    num_test_items = int(math.ceil(test_split*(len(processed_sentences))))

    train_sentences = processed_sentences[:-num_test_items]
    train_labels = labels[:-num_test_items]
    test_sentences = processed_sentences[-num_test_items:]
    test_labels = labels[-num_test_items:]
    # get tfidf features
    Xtrn, Xtst, Ytrn, Ytst = get_tfidf_features(train_sentences, test_sentences,
                                                train_labels, test_labels)


if __name__ == '__main__':
    main()