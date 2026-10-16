import nltk

grammar = nltk.CFG.fromstring("""
                              S -> NP VP
                              NP -> Det N | Det N PP | 'I'
                              VP -> V NP | VP PP
                              PP -> P NP
                              Det -> 'a' | 'the' | 'my'
                              N -> 'cat' | 'dog' | 'bird' | 'park' | 'telescope'
                              V -> 'chased' | 'saw' | 'liked' 
                              P -> 'in' | 'on' | 'by'
                              """)

parser = nltk.ChartParser(grammar)
sentence = "I saw a dog in the park".split()
for tree in parser.parse(sentence):
    print(tree)
    tree.pretty_print()