import nltk
import pandas as pd
from nltk.corpus import stopwords

# expand stopword list as necessary
stop_list = set(stopwords.words("english"))


def add_additional_data(item):
    """ Add additional data to an item in data dictionary
    Args:
        item: A python dictionary containing 'SENTENCE'
    Returns: A python dictionary with additional data.
    """
    sentence = item['SENTENCE']
    sentence = sentence.lower()
    # tokenized sentence after stopword removal
    tokenized_sentence = filter(lambda y: y not in stop_list,
                                nltk.tokenize.word_tokenize(sentence))
    # add processed sentence
    try:
        item['PROCESSED'] = ' '.join(tokenized_sentence)
    except:
        item['PROCESSED'] = ''
    # add more preprocessed data if needed
    return item

def process_data(dataframe):
    """ Preprocess Data
    Args:
        dataframe: A pandas dataframe containing two columns, one for the
            sentence named 'SENTENCE' and another for the label named 'LABEL'.
    Returns: A python dictionary containing processed data.
    """
    raw_data = dataframe.T.to_dict()
    data = {}
    for row_id, row_data in raw_data.iteritems():
        row_data = add_additional_data(row_data)
        data[row_id] = row_data
    return data


def main():
    # read data file
    raw_df = pd.read_csv("filtered_sentences.tsv", sep="\t")
    # preprocess
    data = preprocess.process_data(raw_df)
    raw_sentences = map(lambda x: x['SENTENCE'], data.values())
    processed_sentences = map(lambda x: x['PROCESSED'], data.values())


if __name__ == '__main__':
    main()