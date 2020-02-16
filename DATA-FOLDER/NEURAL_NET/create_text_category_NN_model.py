from numpy import array, argmax
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.optimizers import *
import pickle, os


max_words = 50
tokenizer = Tokenizer(max_words)    

## INIT. DATASET ##
X = []
Y = []
with open('training_text.txt') as f:
    raw_data = f.read()

for i in raw_data.split('\n'):
    data = i.split('=')
    if len(data) != 2:
        continue
    for j in data[0].split('-'):
        X.append(j)
        print(data)
        Y.append(data[1])

CATEGORY = list(sorted(set(Y)))

def topic_to_index(topic_list):
    return [CATEGORY.index(i) for i in topic_list]

tokenizer.fit_on_texts(X)
X_train = tokenizer.texts_to_matrix(X)
print(CATEGORY)
Y_train = to_categorical(topic_to_index(Y), len(set(Y)))
#


## INIT. MODEL ##
model = Sequential([
    Dense(256, activation='relu', input_shape=(max_words,)),
    Dense(256, activation='relu'),
    Dense(len(CATEGORY), activation='sigmoid')
])

model.compile(
    optimizer=Adam(0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

with open('Tokenizer.dat', 'wb') as config_dictionary_file:
  # Step 3
  pickle.dump(tokenizer, config_dictionary_file)

try:
    os.remove('query_category_predictor.neuralNET')
except:
    pass

## TRAINING ##
batch_size = 16
epochs = 500
print(X_train[0])
model.fit(X_train, Y_train, epochs=epochs, verbose=1, shuffle=True)
model.save('query_category_predictor.neuralNET')
model = load_model('query_category_predictor.neuralNET')
print(model.evaluate(X_train, Y_train))
while True:
    text = [input('>> ')]
    text = tokenizer.texts_to_matrix(text)
    res_proba = model.predict(text)
    res = CATEGORY[argmax(model.predict(text))]
    print('TYPE :', res, '       CONFIDENCE :', max(res_proba[0]), res_proba)
