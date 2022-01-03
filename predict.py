import sys
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

MAX_VOCAB_SIZE = 20000
MAX_SEQUENCE_LENGTH = 100


def main():
    model = load_model("model/cnn_model")
    test_text = []
    test_text.append(sys.argv[1])
    tokenizer = Tokenizer(num_words=MAX_VOCAB_SIZE)
    tokenizer.fit_on_texts(test_text)
    test_seq = tokenizer.texts_to_sequences(test_text)
    test_pad = pad_sequences(test_seq, maxlen=MAX_SEQUENCE_LENGTH)
    possible_labels = []
    labels_file = open("model/labels", "r")
    for label in labels_file:
        possible_labels.append(label)
    prediction = model.predict(test_pad)[0].round(1)
    for i in range(len(possible_labels)):
        print(prediction[i], possible_labels[i])


if __name__ == "__main__":
    main()