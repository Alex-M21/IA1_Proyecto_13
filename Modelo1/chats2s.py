import numpy as np
import pandas as pd
import os
import re
from AttentionLayer import AttentionLayer
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Embedding, LSTM, Input, Bidirectional, Concatenate, Dropout
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
import tensorflow as tf

lines = open('dataset/movie_lines.txt', encoding='utf-8', errors='ignore').read().split('\n')
convers = open('dataset/movie_conversations.txt', encoding='utf-8', errors='ignore').read().split('\n')

exchn = []
for conver in convers:
    exchn.append(conver.split(' +++$+++ ')[-1][1:-1].replace("'", " ").replace(",", "").split())

diag = {}
for line in lines:
    diag[line.split(' +++$+++ ')[0]] = line.split(' +++$+++ ')[-1]

del(lines, convers, conver, line)

questions = []
answers = []
for conver in exchn:
    for i in range(len(conver) - 1):
        questions.append(diag[conver[i]])
        answers.append(diag[conver[i + 1]])

del(diag, exchn, conver, i)

sorted_ques = []
sorted_ans = []
for i in range(len(questions)):
    if len(questions[i]) < 13:
        sorted_ques.append(questions[i])
        sorted_ans.append(answers[i])

def clean_text(txt):
    txt = txt.lower()
    txt = re.sub(r"i'm", "i am", txt)
    txt = re.sub(r"he's", "he is", txt)
    txt = re.sub(r"she's", "she is", txt)
    txt = re.sub(r"that's", "that is", txt)
    txt = re.sub(r"what's", "what is", txt)
    txt = re.sub(r"where's", "where is", txt)
    txt = re.sub(r"\'ll", " will", txt)
    txt = re.sub(r"\'ve", " have", txt)
    txt = re.sub(r"\'re", " are", txt)
    txt = re.sub(r"\'d", " would", txt)
    txt = re.sub(r"won't", "will not", txt)
    txt = re.sub(r"can't", "can not", txt)
    txt = re.sub(r"[^\w\s]", "", txt)
    return txt

clean_ques = [clean_text(line) for line in sorted_ques]
clean_ans = [clean_text(line) for line in sorted_ans]

del(answers, questions)

for i in range(len(clean_ans)):
    clean_ans[i] = ' '.join(clean_ans[i].split()[:11])

del(sorted_ans, sorted_ques)

clean_ans = clean_ans[:30000]
clean_ques = clean_ques[:30000]

word2count = {}
for line in clean_ques:
    for word in line.split():
        word2count[word] = word2count.get(word, 0) + 1
for line in clean_ans:
    for word in line.split():
        word2count[word] = word2count.get(word, 0) + 1

del(word, line)

thresh = 5
vocab = {}
word_num = 0
for word, count in word2count.items():
    if count >= thresh:
        vocab[word] = word_num
        word_num += 1

del(word2count, word, count, thresh, word_num)

for i in range(len(clean_ans)):
    clean_ans[i] = '<SOS> ' + clean_ans[i] + ' <EOS>'

tokens = ['<PAD>', '<EOS>', '<OUT>', '<SOS>']
x = len(vocab)
for token in tokens:
    vocab[token] = x
    x += 1
vocab['cameron'] = vocab['<PAD>']
vocab['<PAD>'] = 0

del(token, tokens, x)

inv_vocab = {w: v for v, w in vocab.items()}

del(i)

encoder_inp = []
for line in clean_ques:
    lst = [vocab.get(word, vocab['<OUT>']) for word in line.split()]
    encoder_inp.append(lst)

decoder_inp = []
for line in clean_ans:
    lst = [vocab.get(word, vocab['<OUT>']) for word in line.split()]
    decoder_inp.append(lst)

del(clean_ans, clean_ques, line, lst)

encoder_inp = pad_sequences(encoder_inp, 13, padding='post', truncating='post')
decoder_inp = pad_sequences(decoder_inp, 13, padding='post', truncating='post')

decoder_final_output = []
for i in decoder_inp:
    decoder_final_output.append(i[1:])

decoder_final_output = pad_sequences(decoder_final_output, 13, padding='post', truncating='post')
del(i)

VOCAB_SIZE = len(vocab)
MAX_LEN = 13
decoder_final_output = to_categorical(decoder_final_output, len(vocab))

embeddings_index = {}
with open('dataset/glove.6B.50d.txt', encoding='utf-8') as f:
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs

def embedding_matrix_creater(embedding_dimention, word_index):
    embedding_matrix = np.zeros((len(word_index) + 1, embedding_dimention))
    for word, i in word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
    return embedding_matrix

embedding_matrix = embedding_matrix_creater(50, word_index=vocab)
embed = Embedding(VOCAB_SIZE + 1, 50, input_length=13, trainable=True)
embed.build((None,))
embed.set_weights([embedding_matrix])

enc_inp = Input(shape=(13,))
enc_embed = embed(enc_inp)
enc_lstm = Bidirectional(LSTM(400, return_state=True, dropout=0.05, return_sequences=True))
encoder_outputs, forward_h, forward_c, backward_h, backward_c = enc_lstm(enc_embed)
state_h = Concatenate()([forward_h, backward_h])
state_c = Concatenate()([forward_c, backward_c])
enc_states = [state_h, state_c]

dec_inp = Input(shape=(13,))
dec_embed = embed(dec_inp)
dec_lstm = LSTM(400 * 2, return_state=True, return_sequences=True, dropout=0.05)
output, state_h, state_c = dec_lstm(dec_embed, initial_state=enc_states)

# attention
#attn_layer = AttentionLayer()
#attn_op, attn_state = attn_layer([encoder_outputs, output])
#decoder_concat_input = Concatenate(axis=-1)([output, attn_op])


dec_dense = Dense(VOCAB_SIZE, activation='softmax')
final_output = dec_dense(output)

model = Model([enc_inp, dec_inp], final_output)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
model.fit([encoder_inp, decoder_inp], decoder_final_output, epochs=1, batch_size=24, validation_split=0.15)
model.save('chatbot.h5')
model.save_weights('chatbot.weights.h5')


model_json = model.to_json()
with open("chatbot_model.json", "w") as json_file:
    json_file.write(model_json)


enc_model = tf.keras.models.Model(enc_inp, [encoder_outputs, enc_states])

decoder_input_h = Input(shape=(400 * 2,))
decoder_input_c = Input(shape=(400 * 2,))
decoder_states_inputs = [decoder_input_h, decoder_input_c]

decoder_embedded = embed(dec_inp)
decoder_outputs, state_h, state_c = dec_lstm(decoder_embedded, initial_state=decoder_states_inputs)
#attn_out, attn_states = attn_layer([encoder_outputs, decoder_outputs])
#decoder_concat_output = Concatenate(axis=-1)([decoder_outputs, attn_out])
#decoder_pred = dec_dense(decoder_concat_output)
decoder_pred = dec_dense(decoder_outputs)

dec_model = Model([dec_inp, encoder_outputs, decoder_input_h, decoder_input_c], [decoder_pred, state_h, state_c])

prepro1 = ""
while prepro1 != 'q':
    
    prepro1 = input("you : ")
    prepro = [prepro1]
    
    try:
        txt = []
        for x in prepro:
            lst = []
            for y in x.split():
                lst.append(vocab[y])
            txt.append(lst)
        txt = pad_sequences(txt, 13, padding='post')


        ###
        enc_op, stat = enc_model.predict( txt )

        empty_target_seq = np.zeros( ( 1 , 1) )
        empty_target_seq[0, 0] = vocab['<SOS>']
        stop_condition = False
        decoded_translation = ''


        while not stop_condition :

            dec_outputs , h , c = dec_model.predict([ empty_target_seq ] + stat )

            ###
            ###########################
            attn_op, attn_state = attn_layer([enc_op, dec_outputs])
            decoder_concat_input = Concatenate(axis=-1)([dec_outputs, attn_op])
            decoder_concat_input = dec_dense(decoder_concat_input)
            ###########################

            sampled_word_index = np.argmax( decoder_concat_input[0, -1, :] )

            sampled_word = inv_vocab[sampled_word_index] + ' '

            if sampled_word != '<EOS> ':
                decoded_translation += sampled_word           


            if sampled_word == '<EOS> ' or len(decoded_translation.split()) > 13:
                stop_condition = True

            empty_target_seq = np.zeros( ( 1 , 1 ) )  
            empty_target_seq[ 0 , 0 ] = sampled_word_index
            stat = [ h , c ] 
    except:
        pass

    print("chatbot attention : ", decoded_translation )
    print("==============================================")


