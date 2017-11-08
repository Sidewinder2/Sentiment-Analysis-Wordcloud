
import os
import re
import time
from selenium import webdriver
from Sentiment import Sentiment
from lxml.html import fromstring
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud, STOPWORDS
from selenium.webdriver.common.by import By
from wordcloud_custom_color import wordcloud_custom_color

unusedWords = ["GILBERT","DICAPRIO","FREDDY","ACTORS","GIVES","ACTING","MARTIN","TERRY","LEONARDO","CAST","BURTON",
				"GILLIAM","EDWARD","JOHNNY","DEPP","GEORGE","CLOONEY","MOVIE","FILM","LIKE","REALLY","SEE","MUCH","CAN","JUST","ONE",
				"FIRST","TWO","LOT","DIDNT","DONT","THOUGH","GOOD","GREAT","WELL","GET","ALSO","THATS","SAY","EVEN",
				"MADE","WAY","WILL","BIT","BACK","KNOW","EVER","BETTER","MANY","NEVER","SEEN","DOESNT","MAKES","THINK",
				"NEW","BAD","LOOK","WATCH","MAKE","THERES","ENOUGH","ACTUALLY","THOUGHT","SCENES","IVE","ANOTHER",
				"GOING","CANT","NOTHING","GOT","FIND","THINGS","ISNT","DONE","FILMS","PART","EVERY","TAKE","LITTLE",
				"END","STILL","THING","SOMETHING","QUITE","NOW","RIGHT","HOWEVER","DEFINITELY","FEEL","WANT","MOVIES",
				"TRUE","WORK","FOUND","ENDING","DIRECTOR","AROUND","GIVE","MAN","LIKED","MAY","WASNT","JOB","WITHOUT",
				"SURE","COME","MIGHT","ANYTHING","EVERYTHING","TRYING","YET","ESPECIALLY","FELT","SCENE","FAR","MUST",
				"OVERALL","TIMES","WATCHING","YEARS","ALWAYS","POINT","SINCE","DAY","FACT","HES","GETS","LAST","MINUTES",
				"SCRIPT","SEEMS","SENSE","WORLD","ABOUT","ABOVE","AFTER","AGAIN","AGAINST","ARENT","BECAUSE","BEEN",
				"BEFORE","BEING","BELOW","BETWEEN","BOTH","CANNOT","COULD","COULDNT","DIDNT","DOES","DOESNT","DOING",
				"DOWN","DURING","EACH","ELSE","EVER","FROM","FURTHER","HADNT","HASNT","HAVE","HAVENT","HAVING","HERE",
				"HERES","HERS","HERSELF","HIMSELF","HTTP","INTO","ITSELF","JUST","LIKE","MORE","MOST","MUSTNT","MYSELF",
				"ONCE","ONLY","OTHER","OUGHT","OURS ","OURSELVES","OVER","SAME","SHALL","SHANT","SHOULD","SHOULDNT","SOME",
				"SUCH","THAN","THAT","THATS","THEIR","THEIRS","THEM","THEMSELVES","THEN","THERE","THERES","THESE","THEY",
				"THEYD","THEYLL","THEYRE","THEYVE","THIS","THOSE","THROUGH","UNDER","UNTIL","VERY","WASNT","WERE","WERENT",
				"WHAT","WHATS","WHEN","WHENS","WHERE","WHERES","WHICH","WHILE","WHOM","WITH","WOULD","WOULDNT","YOUR","YOURS",
				"YOURSELF","YOURSELVES"]

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
	print("\"Movie Title\",\"Review\",\"Review Score\",\"Genres\"","\"Actors\"", file=csvFile)
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
					print("\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"" % (movieName, comment.replace("\"", "'"), score, genres, actors), file=csvFile)
	csvFile.close()
	browser.quit()

def createSupportingActorFiles(lines, actor):
	for line in lines[1:]:
		supporting_actors = line.strip()[1:-1].split("\",\"")[-1].split("|")
		for supporting_actor in supporting_actors:
			if supporting_actor.strip() == "" or supporting_actor.startswith("as "):
				continue
			output = open("actorCSVs\\" + re.sub("[\\W]", "", actor + supporting_actor.replace(" ", "_")) + ".csv", "a")
			print(line.strip(), file=output)

if __name__ == "__main__":
	actors = ["george_clooney"] # , "johnny_depp"
	lemmatizer = WordNetLemmatizer()
	for actor in actors:
		getTop10MovieForActor(actor)
		with open(actor + ".csv", "r") as f:
			lines = list(f)
			createSupportingActorFiles(lines, actor)
		for file in os.listdir("actorCSVs"):
			frequencies = Sentiment("".join((rows.strip()[1:-1].split("\",\"")[1]) for rows in list(open("actorCSVs\\" + file, "r")))).analyze()
			for word in unusedWords:
				word = lemmatizer.lemmatize(word)
				frequencies.pop(word, None)
			wc = WordCloud(max_words=50, stopwords=STOPWORDS, margin=10, random_state=1).generate("test")
			wc = wordcloud_custom_color(max_words=50, height=700, width=700).generate_from_frequencies({word: Word._frequency for word, Word in frequencies.items()})
			wc.recolor(frequencies)
			wc.to_file("actorCSVs\\" + file + ".png")
			# os.system(actor + ".png")