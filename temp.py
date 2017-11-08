

from collections import Counter

words = list(open("jd_actorlist.txt"))
counter = Counter(words)
print(counter.most_common(10))

words = list(open("gc_actorlist.txt"))
counter = Counter(words)
print(counter.most_common(10))