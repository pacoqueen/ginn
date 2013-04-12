#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Peter Norvig, eres grande, you motherfucker!
Basado en http://norvig.com/spell-correct.html
"""

import re, collections, string

import string, sys
version = string.split(string.split(sys.version.replace("+", ""))[0], ".")
    # Debian empaqueta la versión con un '+' después del 5 y peta.
if map(int, version) < [2, 5]:
    raise ImportError, "Necesario Python >= 2.5"


class SpellCorrector:
    def __init__(self, texto_muy_muy_grande):
        self.NWORDS = self.train(self.words(texto_muy_muy_grande))
        #NWORDS = train(words(file('big.txt').read()))
        # Usaré mi propia lista de palabras.
        #alphabet = 'abcdefghijklmnopqrstuvwxyz'
        # Usaré string.ascii_lowercase en vez definirlo manualmente como arriba.

    def words(self, text): return re.findall('[a-z]+', text.lower()) 

    def train(self, features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

    def edits1(self, word):
        n = len(word)
        return set([word[0:i]+word[i+1:] for i in range(n)] +   # deletion
                   [word[0:i]+word[i+1]+word[i]+word[i+2:] 
                    for i in range(n-1)] +                      # transposition
                   [word[0:i]+c+word[i+1:] for i in range(n) 
                    for c in string.ascii_lowercase] +          # alteration
                   [word[0:i]+c+word[i:] for i in range(n+1) 
                    for c in string.ascii_lowercase])           # insertion

    def known_edits2(self, word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) 
                    if e2 in self.NWORDS)

    def known(self, words): return set(w for w in words if w in self.NWORDS)

    def correct(self, word):
        candidates = (self.known([word]) or self.known(self.edits1(word)) 
                        or self.known_edits2(word) or [word])
        return max(candidates, key=lambda w: self.NWORDS[w])

if __name__ == "__main__":
    #s = SpellCorrector(file('big.txt').read())
    s = SpellCorrector("""spelling Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque ut nunc mi, vel consectetur nisi. Duis elementum, lorem et sodales convallis, massa ipsum consequat eros, eget semper arcu purus sed dui. Suspendisse eu blandit ligula. Maecenas lobortis orci ut urna iaculis viverra. Fusce ut luctus metus. Phasellus pellentesque libero et risus fermentum congue. Integer dignissim massa porta enim bibendum in imperdiet neque gravida. Morbi mollis nulla sed urna aliquet lacinia. Morbi sed leo vel erat porta feugiat ut at odio. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Etiam malesuada, mi in luctus imperdiet, dolor ante ornare tortor, eget ullamcorper lectus dolor in turpis. Integer hendrerit magna nec est rutrum id sodales purus adipiscing. Etiam aliquam vehicula odio, ut fermentum quam porttitor vitae. Sed consectetur placerat velit, a gravida nulla malesuada in.

Nulla facilisi. Nullam vel arcu massa. Morbi malesuada posuere nunc a blandit. Phasellus velit augue, gravida eget vulputate scelerisque, elementum id risus. Nunc venenatis nunc ut turpis porta placerat. Morbi eu sem at nisl tempor viverra. Suspendisse turpis est, aliquam id dignissim in, tempus in tortor. Praesent eu mi justo, at venenatis quam. Nullam sagittis dolor non lorem ornare cursus. Donec ultrices lacus diam, vitae suscipit sapien. Nullam et mi mi. Suspendisse potenti. Nullam magna nulla, pulvinar vitae convallis vel, sodales non nisl. Vestibulum ultrices eleifend semper.

Vivamus mattis felis a lectus rutrum consectetur. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nam dignissim, tellus quis semper tincidunt, libero quam varius ligula, sit amet ultrices erat lacus vel diam. Aenean dui turpis, condimentum nec tristique in, cursus non mi. Proin feugiat blandit justo vitae rutrum. Etiam semper consequat lacus, vel consequat velit scelerisque nec. Aliquam a purus tellus, nec varius purus. Mauris non auctor ligula. Nunc malesuada metus eget lacus rutrum ut tempus mauris aliquam. Curabitur et leo odio, sed pulvinar sapien. Duis pellentesque commodo quam a venenatis. Suspendisse id nunc sit amet odio tempor auctor. Nulla facilisi. Duis vel libero mi. Aenean posuere viverra egestas. Pellentesque tristique, leo et pellentesque varius, mi leo rutrum orci, sit amet auctor felis elit sit amet eros.

Sed placerat porta quam, quis fringilla risus eleifend sed. Nullam vehicula arcu quis quam consequat lobortis. Morbi eget quam sed orci congue fringilla. Nunc blandit tellus et ligula blandit eleifend. Proin pulvinar diam vel massa scelerisque posuere. Vestibulum luctus enim vitae velit lobortis dictum. Nulla sem diam, gravida eu interdum ut, ultricies in lectus. Vestibulum ullamcorper, dui vel bibendum congue, risus sapien euismod enim, ac fringilla nisl nibh non felis. Suspendisse gravida enim a magna fringilla vitae pulvinar sapien ultrices. Integer scelerisque porta tincidunt.

Pellentesque metus mauris, fringilla non tincidunt porttitor, consequat non lacus. Phasellus a diam lorem, id accumsan metus. In eleifend, neque at fringilla porttitor, arcu mauris fermentum turpis, eget accumsan arcu ipsum vitae ipsum. Vivamus odio tortor, lacinia nec pharetra vitae, ullamcorper et eros. Integer pretium, lectus vitae tempor adipiscing, mi nisi vulputate mauris, ut dictum nulla odio ac purus. Phasellus tempus, lacus quis iaculis convallis, elit ligula commodo mi, vitae porta nulla tellus sit amet ipsum. Mauris arcu justo, imperdiet vitae facilisis in, cursus a lectus. Proin a ipsum vitae metus adipiscing fermentum at ut ante. Quisque luctus purus vel eros bibendum id semper enim molestie. Curabitur in massa et metus commodo sagittis eget vel sem. Maecenas vel vulputate neque. Suspendisse luctus egestas nisi, rutrum ultricies metus elementum at. Nunc metus ipsum, vulputate in vestibulum commodo, semper et massa. Suspendisse eget urna leo. Curabitur elit lacus, consequat sit amet aliquet quis, tincidunt in tellus. Sed et tellus eget elit ullamcorper fermentum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec velit lorem, lacinia id cursus eget, semper eget tellus. """)
    print s.correct("Speling".lower())

