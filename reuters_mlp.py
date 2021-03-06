'''Trains and evaluate a simple MLP
on the Reuters newswire topic classification task.
'''
from __future__ import print_function

import numpy as np
import keras
from keras.datasets import reuters
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.preprocessing.text import Tokenizer
from keras import utils as np_utils
import csv
max_words = 2000
batch_size = 32
epochs = 5
skip_top = 5
test_split = 0.3
num_test = 100
sum_accuracy = 0
with open('results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Test', 'Score', 'Accuracy'])
    for test in range(num_test):
        print('Loading data...')
        (x_train, y_train), (x_test, y_test) = reuters.load_data(num_words=max_words,
                                                                 test_split=test_split, skip_top = skip_top)
        print(len(x_train), 'train sequences')
        print(len(x_test), 'test sequences')

        num_classes = np.max(y_train) + 1
        print(num_classes, 'classes')

        print('Vectorizing sequence data...')
        tokenizer = Tokenizer(num_words=max_words)
        x_train = tokenizer.sequences_to_matrix(x_train, mode='binary')
        x_test = tokenizer.sequences_to_matrix(x_test, mode='binary')
        print('x_train shape:', x_train.shape)
        print('x_test shape:', x_test.shape)

        print('Convert class vector to binary class matrix '
              '(for use with categorical_crossentropy)')
        y_train = keras.utils.np_utils.to_categorical(y_train, num_classes)
        y_test = keras.utils.np_utils.to_categorical(y_test, num_classes)
        print('y_train shape:', y_train.shape)
        print('y_test shape:', y_test.shape)

        print('Building model...')
        model = Sequential()
        model.add(Dense(512, input_shape=(max_words,)))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes))
        model.add(Activation('softmax'))

        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])

        history = model.fit(x_train, y_train,
                            batch_size=batch_size,
                            epochs=epochs,
                            verbose=1,
                            validation_split=0.1)
        score = model.evaluate(x_test, y_test,
                               batch_size=batch_size, verbose=1)

        writer.writerow([test, score[0], score[1]])
        print ('Test number ', test )
        print('Test score:', score[0])
        print('Test accuracy:', score[1])
        sum_accuracy += score[1]
    print('Mean accuracy: ', sum_accuracy/num_test)
