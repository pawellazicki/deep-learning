import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, GlobalMaxPooling1D, Dropout
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.models import Model
from sklearn.metrics import roc_auc_score
from preprocessing import Preprocessing
from keras.utils.vis_utils import plot_model
from matplotlib import pyplot as plt

MAX_SEQUENCE_LENGTH = 200
MAX_VOCAB_SIZE = 30000
EMBEDDING_DIM = 100
VALIDATION_SPLIT = 0.25
BATCH_SIZE = 128
EPOCHS = 5

word2vec = {}
with open(os.path.join('vectors/pl-embeddings-cbow.txt')) as f:
    for line in f:
        values = line.split()
        word = values[0]
        vec = np.asarray(values[1:], dtype='float32')
        word2vec[word] = vec
print('Found %s word vectors.' % len(word2vec))

pr = Preprocessing()
pr.load_data()
pr.clean_text()
pr.remove_stops()

targets = pr.targets
texts = pr.texts
possible_labels = pr.categories
labels_file = open("model/labels", "w")
for label in possible_labels:
    labels_file.write(label + "\n")
labels_file.close()

tokenizer = Tokenizer(num_words=MAX_VOCAB_SIZE)
tokenizer.fit_on_texts(texts)

texts = tokenizer.texts_to_sequences(texts)

print("max text length:", max(len(s) for s in texts))
print("min text length:", min(len(s) for s in texts))
s = sorted(len(s) for s in texts)
print("median text length:", s[len(s) // 2])

print("max word index:", max(max(seq) for seq in texts if len(seq) > 0))

word2idx = tokenizer.word_index
data = pad_sequences(texts, maxlen=MAX_SEQUENCE_LENGTH)

num_words = min(MAX_VOCAB_SIZE, len(word2idx) + 1)
embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
for word, i in word2idx.items():
    if i < MAX_VOCAB_SIZE:
        embedding_vector = word2vec.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

embedding_layer = Embedding(num_words,
                            EMBEDDING_DIM,
                            weights=[embedding_matrix],
                            input_length=MAX_SEQUENCE_LENGTH,
                            trainable=False)

# CNN model
input_ = Input(shape=(MAX_SEQUENCE_LENGTH, ))
x = embedding_layer(input_)
x = Conv1D(128, 3, activation='relu')(x)
x = MaxPooling1D(3)(x)
x = Conv1D(128, 3, activation='relu')(x)
x = MaxPooling1D(3)(x)
x = Conv1D(128, 3, activation='relu')(x)
x = GlobalMaxPooling1D()(x)
x = Dense(128, activation='relu')(x)
output = Dense(len(possible_labels), activation='softmax')(x)

model = Model(input_, output)
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

dot_img_file = 'model_1.png'
plot_model(model, to_file=dot_img_file, show_shapes=True)

print('Training model...')
history = model.fit(data,
                    targets,
                    batch_size=BATCH_SIZE,
                    epochs=EPOCHS,
                    validation_split=VALIDATION_SPLIT)

# Accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

# Loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

model.save("model/cnn_model")