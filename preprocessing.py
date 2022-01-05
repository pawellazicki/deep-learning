import re
import nltk
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import random


class Preprocessing:
    def __init__(self):
        self.data = 'Output_44k.txt'
        self.texts = None
        self.targets = None

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
        self.texts = df['text'].values
        self.targets = df['target'].values

        zipped = list(zip(self.texts, self.targets))
        random.shuffle(zipped)
        zipped = filter(lambda item: item[0] != '\n', zipped)
        self.texts, self.targets = map(np.array, zip(*zipped))

        zeros = np.zeros(len(self.categories), dtype=int)
        targets_zeros = [zeros.copy() for _ in self.targets]

        for i in range(len(targets_zeros)):
            targets_zeros[i][self.categories.index(self.targets[i])] = 1
        self.targets = np.array(targets_zeros)

    def clean_text(self):

        self.texts = [x.lower() for x in self.texts]
        self.texts = [
            re.sub(r'\s+[A-Za-ząęźćśółżń]\s+', ' ', x) for x in self.texts
        ]
        self.texts = [
            re.sub(r'[^A-Za-ząęźćśółżń]+', ' ', x) for x in self.texts
        ]
        # self.texts = [x.replace('ą', 'a') for x in self.texts]
        # self.texts = [x.replace('ę', 'e') for x in self.texts]
        # self.texts = [x.replace('ź', 'z') for x in self.texts]
        # self.texts = [x.replace('ż', 'z') for x in self.texts]
        # self.texts = [x.replace('ć', 'c') for x in self.texts]
        # self.texts = [x.replace('ś', 's') for x in self.texts]
        # self.texts = [x.replace('ó', 'o') for x in self.texts]
        # self.texts = [x.replace('ł', 'l') for x in self.texts]
        # self.texts = [x.replace('ń', 'n') for x in self.texts]
        # self.texts = [re.sub(r'\s+[A-Za-z]\s+', ' ', x) for x in self.texts]
        # self.texts = [re.sub(r'[^A-Za-z]+', ' ', x) for x in self.texts]

    def remove_stops(self):
        stops = stopwords.words('polish')
        for idx, text in enumerate(self.texts):
            text_tokens = word_tokenize(text)
            self.texts[idx] = [
                word for word in text_tokens if not word in stops
            ]
            self.texts[idx] = ' '.join(self.texts[idx])
