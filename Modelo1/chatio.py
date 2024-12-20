import re
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Dense, Embedding, LSTM, Input
from keras.models import Model

with open('dataset/movie_lines.txt', encoding='utf-8', errors='ignore') as file:
    lines = file.read().split('\n')

with open('dataset/movie_conversations.txt', encoding='utf-8', errors='ignore') as file2:
    conversations = file2.read().split('\n')

exchange = []
dialogue = {}
questions = []
answers = []
sorted_ques = []
sorted_ans = []
clean_ques = []
clean_ans = []

for conversation in conversations:
    tmp = conversation.split(' +++$+++ ')[-1][1:-1].replace("'", "").replace(",", "")
    exchange.append(tmp.split())

for line in lines:
    tmp = line.split(' +++$+++ ')
    dialogue[tmp[0]] = tmp[-1]

for conv in exchange:
    for i in range(len(conv) - 1):
        questions.append(dialogue[conv[i]])
        answers.append(dialogue[conv[i + 1]])

for i in range(len(questions)):
    if len(questions[i]) <= 13:
        sorted_ques.append(questions[i])
        sorted_ans.append(answers[i])

def clean_text(txt):
    contractions = {
        r"i'm": "i am",
        r"he's": "he is",
        r"she's": "she is",
        r"that's": "that is",
        r"what's": "what is",
        r"where's": "where is",
        r"who's": "who is",
        r"how's": "how is",
        r"let's": "let us",
        r"i'll": "i will",
        r"he'll": "he will",
        r"she'll": "she will",
        r"we'll": "we will",
        r"you'll": "you will",
        r"they'll": "they will",
        r"i've": "i have",
        r"you've": "you have",
        r"we've": "we have",
        r"they've": "they have",
        r"you're": "you are",
        r"we're": "we are",
        r"they're": "they are",
        r"i'd": "i would",
        r"you'd": "you would",
        r"he'd": "he would",
        r"she'd": "she would",
        r"we'd": "we would",
        r"they'd": "they would",
        r"won't": "will not",
        r"can't": "cannot",
        r"shouldn't": "should not",
        r"wouldn't": "would not",
        r"couldn't": "could not",
        r"haven't": "have not",
        r"hasn't": "has not",
        r"hadn't": "had not",
        r"isn't": "is not",
        r"aren't": "are not",
        r"wasn't": "was not",
        r"weren't": "were not",
        r"doesn't": "does not",
        r"don't": "do not",
        r"didn't": "did not",
    }

    txt = txt.lower()
    for contraction, replacement in contractions.items():
        txt = re.sub(contraction, replacement, txt)
    txt = re.sub(r"[^\w\s]", "", txt)
    return txt

for line in sorted_ques:
    clean_ques.append(clean_text(line))

for line in sorted_ans:
    clean_ans.append(clean_text(line))

for i in range(len(clean_ques)):
    clean_ans[i] = ' '.join(clean_ans[i].split()[:11])

clean_ans = clean_ans[:10000]
clean_ques = clean_ques[:10000]

word2count = {}
for line in clean_ques:
    for word in line.split():
        word2count[word] = word2count.get(word, 0) + 1
for line in clean_ans:
    for word in line.split():
        word2count[word] = word2count.get(word, 0) + 1

thresh = 2
vocab = {}
word_num = 0
for word, count in word2count.items():
    if count >= thresh:
        vocab[word] = word_num
        word_num += 1

for token in ['<PAD>', '<EOS>', '<OUT>', '<SOS>']:
    vocab[token] = len(vocab)

inv_vocab = {v: w for w, v in vocab.items()}

for i in range(len(clean_ans)):
    clean_ans[i] = '<SOS> ' + clean_ans[i] + ' <EOS>'

encoder_inp = []
for line in clean_ques:
    lst = []
    for word in line.split():
        lst.append(vocab.get(word, vocab['<OUT>']))
    encoder_inp.append(lst)

decoder_inp = []
for line in clean_ans:
    lst = []
    for word in line.split():
        lst.append(vocab.get(word, vocab['<OUT>']))
    decoder_inp.append(lst)

encoder_inp = pad_sequences(encoder_inp, 13, padding='post', truncating='post')
decoder_inp = pad_sequences(decoder_inp, 13, padding='post', truncating='post')

decoder_final_output = []
for i in decoder_inp:
    decoder_final_output.append(i[1:])
decoder_final_output = pad_sequences(decoder_final_output, 13, padding='post', truncating='post')
decoder_final_output = to_categorical(decoder_final_output, len(vocab))

enc_inp = Input(shape=(13,))
dec_inp = Input(shape=(13,))

VOCAB_SIZE = len(vocab)
embed = Embedding(VOCAB_SIZE+1, output_dim=50, input_length=13, trainable=True)

enc_embed = embed(enc_inp)
enc_lstm = LSTM(400, return_sequences=True, return_state=True)
enc_op, h, c = enc_lstm(enc_embed)
enc_states = [h, c]

dec_embed = embed(dec_inp)
dec_lstm = LSTM(400, return_sequences=True, return_state=True)
dec_op, _, _ = dec_lstm(dec_embed, initial_state=enc_states)

dense = Dense(VOCAB_SIZE, activation='softmax')
dense_op = dense(dec_op)

model = Model([enc_inp, dec_inp], dense_op)
model.compile(loss='categorical_crossentropy', metrics=['acc'], optimizer='adam')
model.fit([encoder_inp, decoder_inp], decoder_final_output, epochs=10)

def chatbot_response(input_text):
    input_text = clean_text(input_text)
    input_seq = [vocab.get(word, vocab['<OUT>']) for word in input_text.split()]
    input_seq = pad_sequences([input_seq], maxlen=13, padding='post', truncating='post')

    output_seq = np.zeros((1, 13), dtype=int)
    output_seq[0, 0] = vocab['<SOS>']

    response = []
    for i in range(1, 13):
        predicted = model.predict([input_seq, output_seq])
        token_id = np.argmax(predicted[0, i - 1])
        response.append(inv_vocab[token_id])
        if inv_vocab[token_id] == '<EOS>':
            break
        output_seq[0, i] = token_id

    return ' '.join(response)

def chat():
    print("¡Hola! Soy un chatbot. Escribe 'salir' para terminar la conversación.")
    while True:
        user_input = input("Tú: ")
        if user_input.lower() == "salir":
            print("¡Adiós!")
            break
        response = chatbot_response(user_input)
        print("Chatbot:", response)

chat()
