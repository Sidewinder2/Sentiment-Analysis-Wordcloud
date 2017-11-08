


import nltk
#nltk.download()

#
# EXAMPLE_TEXT = "Hello Mr. Smith, how are you doing today? The weather is great, and Python is awesome. The sky is pinkish-blue. You shouldn't eat cardboard."
# #
# print(word_tokenize(EXAMPLE_TEXT))


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    #note: depending on how you installed (e.g., using source code download versus pip install), you may need to import like this:
    #from vaderSentiment import SentimentIntensityAnalyzer

# --- examples -------
# sentences = ["VADER is smart, handsome, and funny.",      # positive sentence example
#             "VADER is not smart, handsome, nor funny.",   # negation sentence example
#             "VADER is smart, handsome, and funny!",       # punctuation emphasis handled correctly (sentiment intensity adjusted)
#             "VADER is very smart, handsome, and funny.",  # booster words handled correctly (sentiment intensity adjusted)
#             "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
#             "VADER is VERY SMART, handsome, and FUNNY!!!",# combination of signals - VADER appropriately adjusts intensity
#             "VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!",# booster words & punctuation make this close to ceiling for score
#             "The book was good.",                                     # positive sentence
#             "The book was kind of good.",                 # qualified positive sentence is handled correctly (intensity adjusted)
#             "The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
#             "At least it isn't a horrible book.",         # negated negative sentence with contraction
#             "Make sure you :) or :D today!",              # emoticons handled
#             "Today SUX!",                                 # negative slang with capitalization emphasis
#             "Today only kinda sux! But I'll get by, lol", # mixed sentiment example with slang and constrastive conjunction "but"
#             "I like donuts, but only on Tuesday",
#             "I like donuts",
#             "I really like donuts",
#              "So bad it's good"
#              ]

from nltk.tokenize import sent_tokenize, word_tokenize

class Word:
    def __init__(self, wordstr):
        self.wordstr = wordstr
        self.wordcount = 0  # number of times word has been used
        self.word_totals = [0,0,0,0]    # total of all word scores
        self.word_mins = [0,0,0,0]  # lowest score word has received
        self.word_maxes = [0,0,0,0] # highest score word has received

    def get_wordcount(self):
        return self.wordcount

    def add_totals(self,totals):
        # add totals to score
        for i in range(0,len(totals)):
            self.word_totals[i] += totals[i]
        self.wordcount += 1

    def get_totals(self):
        return self.word_totals

    def get_avg_totals(self):
        returnlist = self.word_totals
        if self.wordcount > 0:
            for i in range(0,len(returnlist)):
                returnlist[i] = returnlist[i] / self.wordcount
        return returnlist

    def get_mins(self):
        return self.word_mins

    def get_maxes(self):
        return self.word_maxes

word_store = {} # Maintains dict of word pointers

filename = 'george_clooney.csv'
file = open(filename, 'r')
sentences = file.readlines()

analyzer = SentimentIntensityAnalyzer()

for index in range(1,len(sentences)):
    # get review sentence
    sentence = sentences[index].split('","')[1]
    print(sentence)

    # analyze it
    vs = analyzer.polarity_scores(sentence)
    # had to make a copy of vs that actually supports indexing
    values = []
    for v in vs.values():
        values.append(v)

    # go through sentence adding in newly found words, and updating scores
    for word in word_tokenize(sentence):
        if word.lower() not in word_store.keys():
            w = Word(word.lower())
            w.add_totals(values)
            word_store[word.lower()] = w
        else:
            w = word_store[word.lower()]
            w.add_totals(values)

for word in word_store.keys():
    w = word_store[word]
    if w.get_wordcount() > 3:
        print(word,w.get_avg_totals())




#---------------------------------------------
#This code converts any word into its base form
# from nltk.stem import WordNetLemmatizer
#
# lemmatizer = WordNetLemmatizer()
#
# print(lemmatizer.lemmatize("cats"))
# print(lemmatizer.lemmatize("cacti"))
# print(lemmatizer.lemmatize("geese"))
# print(lemmatizer.lemmatize("rocks"))
# print(lemmatizer.lemmatize("python"))
# print(lemmatizer.lemmatize("better", pos="a"))
# print(lemmatizer.lemmatize("best", pos="a"))
# print(lemmatizer.lemmatize("run"))
# print(lemmatizer.lemmatize("run",'v'))

