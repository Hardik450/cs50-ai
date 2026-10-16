import markovify
import nltk

with open("cris.txt", 'r') as f:
    text = f.read()

model = markovify.Text(text, state_size=2)
for _ in range(5):
    print(model.make_sentence())