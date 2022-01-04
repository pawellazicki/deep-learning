test_seq = tokenizer.texts_to_sequences(text)
test_pad = pad_sequences(test_seq, maxlen=MAX_SEQUENCE_LENGTH)
prediction = model.predict(test_pad)[0].round(1)
for i in range(len(possible_labels)):
    print(possible_labels[i], prediction[i])
