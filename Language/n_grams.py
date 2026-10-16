import nltk
nltk.download('punkt_tab')
sentence = "the cat chased the dog"
tokens = nltk.word_tokenize(sentence)
n_grams= nltk.ngrams(tokens, 2)
print(list(n_grams))