
import os
import re
import time
from selenium import webdriver
from Sentiment import Sentiment

from lxml.html import fromstring
from nltk import WordNetLemmatizer, word_tokenize
from wordcloud import WordCloud, STOPWORDS
from selenium.webdriver.common.by import By
#from wordcloud_custom_color import wordcloud_custom_color
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob



# Chrome setting to remove initial notifications from popping up with each new browser
def setupDriver():
	chrome_options = webdriver.ChromeOptions()
	prefs = {"profile.default_content_setting_values.notifications" : 2}
	chrome_options.add_experimental_option("prefs", prefs)
	return webdriver.Chrome(chrome_options=chrome_options)

def getTop10MovieForActor(actor):
	baseURL = "https://www.rottentomatoes.com"
	endOfURL = "/reviews/?type=user&page="
	links = []
	# setup the selenium driver and go to the web address with all movies
	browser = setupDriver()
	browser.get("https://www.rottentomatoes.com/celebrity/" + actor)
	# Order movies by rating
	browser.find_elements(By.CSS_SELECTOR, ".filmographyTbl_ratingCol > a")[0].click()
	time.sleep(1)
	csvFile = open(actor + ".csv", "w")
	print("\"Movie Title\",\"Review\",\"Review Score\",\"Genres\"","\"Actors\"")
	for i, movieRow in enumerate(browser.find_elements(By.CSS_SELECTOR, "#filmographyTbl > tbody > tr")):
		links.append(movieRow.find_element(By.CSS_SELECTOR, "td > .articleLink").get_attribute("href"))
		# if i == 10:
		# 	break
	for link in links:
		browser.get(link)
		actorHTML = fromstring(browser.page_source)
		actors = "|".join([actorEl.text_content().lower().strip() for actorEl in actorHTML.cssselect("div[class='cast-item media inlineBlock '] a > span[title]")])
		if not any([actor in actors for actor in ["matt damon","brad pitt","don cheadle","julia roberts","bill murray","jennifer aniston","john goodman","julianne moore","juliette lewis","mark wahlberg"]]):
			continue
		actors.replace(actor.lower(), "").replace("||", "")
		movieName = browser.current_url.split("/")[-1]
		count = page = 0
		while count < 50 and page < 10:
			page += 1
			browser.get(link + endOfURL + str(page))
			commentHTML = fromstring(browser.page_source)
			genres = ", ".join([genreEl.text_content() for genreEl in commentHTML.cssselect("#main_container > div > section > div > div.bottom_divider > ul > li > a > span")])
			for commentRow in commentHTML.cssselect(".review_table > div"):
				review = commentRow.cssselect(".user_review")[0]
				comment = review.text_content().strip()
				score = review.cssselect(".scoreWrapper > span")[0].get("class")
				# Make sure there is a score [want to see is an option]
				if re.match("^\d+$", score):
					count += 1
					print("\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"" % (movieName, comment.replace("\"", "'"), score, genres, actors))
	csvFile.close()
	browser.quit()

def createSupportingActorFiles(lines, actor):
	for line in lines[1:]:
		supporting_actors = line.strip()[1:-1].split("\",\"")[-1].split("|")
		for supporting_actor in supporting_actors:
			if supporting_actor.strip() == "" or supporting_actor.startswith("as "):
				continue
			output = open("actorCSVs\\" + re.sub("[\\W]", "", actor + supporting_actor.replace(" ", "_")) + ".csv", "a")
			output.write(line.strip())
			output.close()


def get_actor_reviews(review_file):
	# Pull reviews from actor CSV file. Returns as one string
	raw_text = ""
	actor_file = open(review_file, "r").readlines()	# read the file
	file_str = "".join(actor_file)	# Convert it to string
	lines = file_str.strip()[1:-1].split("\",\"")	# remove bloat text, chop off first and last character, then split
	review_lines = lines[1::4]	# get every 4th line, which contains the review
	for review in review_lines:
		raw_text += review

	return raw_text

def get_stopwords_fromfile(filename):
	stopwords = list()
	lines = open(filename, "r").readlines()  # read the file
	for line in lines:
		stopwords.append(line.strip("\n"))
	return stopwords


def lemmatized_frequencies(raw_text, stopwords = []):
	frequencies = dict()
	lemmatizer = WordNetLemmatizer()
	for sentence in re.split("\\.+ ?", raw_text):
		sentence = re.sub("[,!()-?']", " ", sentence)
		for word in re.split(" +", sentence):
			word = lemmatizer.lemmatize(word.upper())
			if len(word) > 3 and word not in stopwords and word not in STOPWORDS:
				if word in frequencies:
					frequencies[word] = frequencies[word] + 1
				else:
					frequencies[word] = 0

	return frequencies

if __name__ == "__main__":
	actors = ["george_clooney"] # , "johnny_depp"
	lemmatizer = WordNetLemmatizer()


	stopwords = get_stopwords_fromfile("stopwords.txt")
	print(stopwords)


	# run through every actor generating CSVs and word clouds for pairs
	for actor in actors:
		#getTop10MovieForActor(actor)
		with open(actor + ".csv", "r") as f:
			lines = list(f)
			#createSupportingActorFiles(lines, actor)
		for file in os.listdir("actorCSVs"):

			raw_text = get_actor_reviews("actorCSVs\\" + file)

			# get average sentiment
			sentiment = TextBlob(raw_text).sentiment.polarity
			print(file,sentiment)

			# frequencies = Sentiment(raw_text).analyze()

			# generate word clouds
			#wc = WordCloud(max_words=50, stopwords=STOPWORDS, margin=10, random_state=1).generate("test")
			# print(file, frequencies)

			# wc = wordcloud_custom_color(max_words=20, height=700, width=700).generate_from_frequencies({word: Word._frequency for word, Word in frequencies.items()})
			# wc.recolor(frequencies)


			#words = list(set(word_tokenize(raw_text)))
			frequencies = lemmatized_frequencies(raw_text, stopwords)
			# generate wordcloud
			wc = WordCloud(max_words= 50,width=1800, height=1400).generate_from_frequencies(frequencies)
			wc.to_file("actorWordClouds\\" + file + ".png")


			# os.system(actor + ".png")
