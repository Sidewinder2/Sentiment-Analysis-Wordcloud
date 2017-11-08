
import numpy as np
from random import Random
from wordcloud import WordCloud

class wordcloud_custom_color(WordCloud):

	def recolor(self, frequencies, random_state=None, color_func=None, colormap=None):
		
		if isinstance(random_state, int):
			random_state = Random(random_state)
		self._check_generated()

		custom_color = custom_color_func(frequencies)
		self.layout_ = [(word_freq, font_size, position, orientation,
						 custom_color(word=word_freq[0], font_size=font_size,
									position=position, orientation=orientation,
									random_state=random_state,
									font_path=self.font_path))
						for word_freq, font_size, position, orientation, _
						in self.layout_]

		return self

class custom_color_func(object):

	def __init__(self, frequencies):
		self._frequencies = frequencies
		self._max = max([abs(Word._total_score / Word._frequency) for word, Word in frequencies.items()])

	def __call__(self, word, font_size, position, orientation,
				 random_state=None, font_path=None):

		# off = int((self._frequency_map[word] / self._max) * 255)
		# print(word, self._frequency_map[word], off)
		off = int((self._frequencies[word]._total_score / self._frequencies[word]._frequency) * 255)
		off_abs = abs(off)
		# Negative
		if off < 0:
			return "rgb({:.0f}, {:.0f}, {:.0f})".format(255, off_abs, off_abs)

		# Positive
		else:
			return "rgb({:.0f}, {:.0f}, {:.0f})".format(off_abs, 255, off_abs)