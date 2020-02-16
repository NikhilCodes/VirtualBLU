from tensorflow.keras.models import load_model
from pickle import load
from random import choice
from numpy import argmax

from CORE.WOLFRAM_query import get_wolfram_responses

text_classifier = load_model('DATA-FOLDER/NEURAL_NET/query_category_predictor.neuralNET')
text_classifier._make_predict_function()  # ALLOWS PREDICTION ON THREAD
text_tokenizer = load(open('DATA-FOLDER/NEURAL_NET/Tokenizer.dat', 'rb'))
RESPONSE_DICT = load(open('DATA-FOLDER/RESPONSE DATA/response.dat', 'rb'))

# CREDENTIALS
with open("BLU UserDATA/UserInf0.config") as f:
    data = f.read().split('\n')

fname = data[0].split('=')[1]
uname = data[1].split('=')[1]
email = data[2].split('=')[1]


def respond_text(query):
    speech = ''
    if query == '':
        resp = ''
    else:
        X = text_tokenizer.texts_to_matrix([query])
        Y = text_classifier.predict(X)
        category = argmax(Y)
        if category == 3:
            return get_wolfram_responses(query)
            
        resp, speech = [choice(RESPONSE_DICT[category]).replace('<#uname#>', uname).replace('<#fname#>', fname).replace('<#email#>', email)] * 2

    return [[resp], speech]


if __name__ == '__main__':
    while 1:
        print(respond_text(input('>')))
