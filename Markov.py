import string
import random


class Markov:
    
    def __init__(self):
        self.suffix_map = {}
        self.prefix = ()

    def process_word(self, word, order =2):
        
        if len(self.prefix) < order:
            self.prefix += (word,)
            return
        try:
            self.suffix_map[self.prefix].append(word)
        except KeyError:
            #if thre is no entry for this prefix, make one
            self.suffix_map[self.prefix] = [word]
        
        self.prefix = self.shift(self.prefix, word)

    def process_file(self, filename, order = 2):

        fp = open(filename)
        self.skip_gutenberg_header(fp)

        for line in fp:
            for word in line.rstrip().split():
                self.process_word(word, order)

    def skip_gutenberg_header(self, fp):
        for line in fp:
            if line.startswith("*END*THE SMALL PRINT!"):
                break

    def shift(self, t, word):
        return t[1:] + (word,)

    def random_text(self, n=100):
        start = random.choice(list(self.suffix_map.keys()))
        
        for i in range(n):
            suffixes = self.suffix_map.get(start, None)
            if suffixes == None:
                self.random_text(n-i)
                return

            word = random.choice(suffixes)
            print(word, end=" ")
            start = self.shift(start,word)

res = Markov()
res.process_file("emma.txt",2) 
res.random_text(100)
print()           
            
