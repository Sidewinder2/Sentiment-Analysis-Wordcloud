
import re
import nltk
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class Sentiment(object):

	def __init__(self, raw_text):
		self._raw = raw_text

	def analyze(self):
		frequencies = dict()
		lemmatizer = WordNetLemmatizer()
		analyzer = SentimentIntensityAnalyzer()
		for sentence in re.split("\\.+ ?", self._raw):
			score = analyzer.polarity_scores(sentence)["compound"]
			sentence = sentence.replace("n't", " not")
			sentence = sentence.replace("\\bwo not\\b", "will not")
			sentence = re.sub("[,!()-?']", " ", sentence)
			for word in re.split(" +", sentence):
				word = lemmatizer.lemmatize(word.upper())
				if len(word) > 3:
					word = Word(word, score)
					if word._word in frequencies:
						frequencies[word._word].add_to_score(score)
						frequencies[word._word].add_appearance()
					else:
						frequencies[word._word] = word

		return frequencies


class Word(object):

	def __init__(self, word, score):
		self._word = word
		self._total_score = score
		self._frequency = 1
	
	def add_appearance(self):
		self._frequency += 1

	def add_to_score(self, score):
		self._total_score += score

	def __eq__(self, other):
		return self._word == other._word

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return "%s: %s:" % (self._total_score, self._frequency)