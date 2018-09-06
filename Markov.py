import string
import random

class Markov:
    
    def __init__(self):
        self.suffix_map = {}
        self.prefix = ()

    def process_word(self, word, order =2):
        """
        Function to add relevant suffix to suffix_map depending on which prefix the word follows
        order: number of words per prefix
        """
        #add words to prefix to get the 'order' as defined in function parameters
        if len(self.prefix) < order: 
            self.prefix += (word,)
            return
        #map prefixes to suffixes
        try:
            self.suffix_map[self.prefix].append(word)
        except KeyError:
            #if thre is no entry for this prefix, make one
            self.suffix_map[self.prefix] = [word]
        
        self.prefix = self.shift(self.prefix, word)

    def process_file(self, filename, order = 2):
        """
        performs 'process_word' for each word in file
        """
        fp = open(filename)
        self.skip_gutenberg_header(fp)

        for line in fp:
            for word in line.rstrip().split():
                self.process_word(word, order)

    def skip_gutenberg_header(self, fp):
        """
        skips the small print for gutenberg project text
        """
        for line in fp:
            if line.startswith("*END*THE SMALL PRINT!"):
                break

    def shift(self, t, word):
        """moves focus along one word"""
        return t[1:] + (word,)

    def random_text(self, n=100):
        """
        creates random text based on the prefix and suffix maps
        n: length of text
        """
        #select random prefix
        start = random.choice(list(self.suffix_map.keys()))
        
        #choose following word from suffix map, shift prefix window along by 1. Repeat
        for i in range(n):
            suffixes = self.suffix_map.get(start, None)
            if suffixes == None:
                self.random_text(n-i)
                return

            word = random.choice(suffixes)
            print(word, end=" ")
            start = self.shift(start,word)

if __name__ == "__main__":
    res = Markov()
    res.process_file("emma.txt",2) 
    res.random_text(100)
    print()           
            
