import re
import nltk
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

from parameters import Parameters


class Preprocessing:
    def __init__(self, num_words, seq_len):
        self.data = 'Output.txt'
        self.num_words = num_words
        self.seq_len = seq_len
        self.vocabulary = None
        self.x_tokenized = None
        self.x_padded = None
        self.x_raw = None
        self.y = None

        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None
        self.separator_category = '(=-=-=-)'
        self.separator_article = '-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=-\\=\n'
        self.categories = []

    def load_data(self):
        articles = [[], []]
        with open(self.data) as file:
            for line in file:
                text = line.replace(self.separator_article,
                                    '').split(self.separator_category)
                if (len(text) > 1):
                    articles[0].append(text[0])
                    articles[1].append(text[1])
        self.categories = list(set(articles[0]))
        df = pd.DataFrame(articles, index=['target', 'text']).T
        self.x_raw = df['text'].values
        self.y = df['target'].values
        self.y = [self.categories.index(target) for target in self.y]

    def clean_text(self):
        # Removes special symbols and just keep
        # words in lower or upper form

        self.x_raw = [x.lower() for x in self.x_raw]
        self.x_raw = [
            re.sub(r'\^[A-Za-ząęźćśółżń]\s+', ' ', x) for x in self.x_raw
        ]
        self.x_raw = [
            re.sub(r'[^A-Za-ząęźćśółżń]+', ' ', x) for x in self.x_raw
        ]

    def text_tokenization(self):
        # Tokenizes each sentence by implementing the nltk tool
        self.x_raw = [word_tokenize(x) for x in self.x_raw]

    def build_vocabulary(self):
        # Builds the vocabulary and keeps the "x" most frequent words
        self.vocabulary = dict()

        fdist = nltk.FreqDist()
        stops = stopwords.words('polish')
        for sentence in self.x_raw:
            for word in sentence:
                if (word not in stops):
                    fdist[word] += 1

        common_words = fdist.most_common(self.num_words)

        for idx, word in enumerate(common_words):
            self.vocabulary[word[0]] = (idx + 1)

    def word_to_idx(self):
        # By using the dictionary (vocabulary), it is transformed
        # each token into its index based representation

        self.x_tokenized = list()
        for sentence in self.x_raw:
            temp_sentence = list()
            for word in sentence:
                if word in self.vocabulary.keys():
                    temp_sentence.append(self.vocabulary[word])
            self.x_tokenized.append(temp_sentence)

    def padding_sentences(self):
        # Each sentence which does not fulfill the required len
        # it's padded with the index 0

        pad_idx = 0
        self.x_padded = list()
        self.seq_len = 0
        for sentence in self.x_tokenized:
            if len(sentence) > self.seq_len:
                self.seq_len = len(sentence)
        Parameters.seq_len = self.seq_len
        for sentence in self.x_tokenized:
            while len(sentence) < self.seq_len:
                sentence.insert(len(sentence), pad_idx)
            self.x_padded.append(sentence)

        self.x_padded = np.array(self.x_padded)

    def split_data(self):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.x_padded, self.y, test_size=0.25, random_state=42)
