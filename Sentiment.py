
import re
import nltk
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS

class Sentiment(object):
	unusedWords = ["GILBERT", "DICAPRIO", "FREDDY", "ACTORS", "GIVES", "ACTING", "MARTIN", "TERRY", "LEONARDO", "CAST",
				   "BURTON",
				   "GILLIAM", "EDWARD", "JOHNNY", "DEPP", "GEORGE", "CLOONEY", "MOVIE", "FILM", "LIKE", "REALLY", "SEE",
				   "MUCH", "CAN", "JUST", "ONE",
				   "FIRST", "TWO", "LOT", "DIDNT", "DONT", "THOUGH", "GOOD", "GREAT", "WELL", "GET", "ALSO", "THATS",
				   "SAY", "EVEN",
				   "MADE", "WAY", "WILL", "BIT", "BACK", "KNOW", "EVER", "BETTER", "MANY", "NEVER", "SEEN", "DOESNT",
				   "MAKES", "THINK",
				   "NEW", "BAD", "LOOK", "WATCH", "MAKE", "THERES", "ENOUGH", "ACTUALLY", "THOUGHT", "SCENES", "IVE",
				   "ANOTHER",
				   "GOING", "CANT", "NOTHING", "GOT", "FIND", "THINGS", "ISNT", "DONE", "FILMS", "PART", "EVERY",
				   "TAKE", "LITTLE",
				   "END", "STILL", "THING", "SOMETHING", "QUITE", "NOW", "RIGHT", "HOWEVER", "DEFINITELY", "FEEL",
				   "WANT", "MOVIES",
				   "TRUE", "WORK", "FOUND", "ENDING", "DIRECTOR", "AROUND", "GIVE", "MAN", "LIKED", "MAY", "WASNT",
				   "JOB", "WITHOUT",
				   "SURE", "COME", "MIGHT", "ANYTHING", "EVERYTHING", "TRYING", "YET", "ESPECIALLY", "FELT", "SCENE",
				   "FAR", "MUST",
				   "OVERALL", "TIMES", "WATCHING", "YEARS", "ALWAYS", "POINT", "SINCE", "DAY", "FACT", "HES", "GETS",
				   "LAST", "MINUTES",
				   "SCRIPT", "SEEMS", "SENSE", "WORLD", "ABOUT", "ABOVE", "AFTER", "AGAIN", "AGAINST", "ARENT",
				   "BECAUSE", "BEEN",
				   "BEFORE", "BEING", "BELOW", "BETWEEN", "BOTH", "CANNOT", "COULD", "COULDNT", "DIDNT", "DOES",
				   "DOESNT", "DOING",
				   "DOWN", "DURING", "EACH", "ELSE", "EVER", "FROM", "FURTHER", "HADNT", "HASNT", "HAVE", "HAVENT",
				   "HAVING", "HERE",
				   "HERES", "HERS", "HERSELF", "HIMSELF", "HTTP", "INTO", "ITSELF", "JUST", "LIKE", "MORE", "MOST",
				   "MUSTNT", "MYSELF",
				   "ONCE", "ONLY", "OTHER", "OUGHT", "OURS ", "OURSELVES", "OVER", "SAME", "SHALL", "SHANT", "SHOULD",
				   "SHOULDNT", "SOME",
				   "SUCH", "THAN", "THAT", "THATS", "THEIR", "THEIRS", "THEM", "THEMSELVES", "THEN", "THERE", "THERES",
				   "THESE", "THEY",
				   "THEYD", "THEYLL", "THEYRE", "THEYVE", "THIS", "THOSE", "THROUGH", "UNDER", "UNTIL", "VERY", "WASNT",
				   "WERE", "WERENT",
				   "WHAT", "WHATS", "WHEN", "WHENS", "WHERE", "WHERES", "WHICH", "WHILE", "WHOM", "WITH", "WOULD",
				   "WOULDNT", "YOUR", "YOURS",
				   "YOURSELF", "YOURSELVES"]


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
				if len(word) > 3 and word not in Sentiment.unusedWords and word not in STOPWORDS:
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
		return "%s: %s:" % (self._total_score / self._frequency, self._frequency)