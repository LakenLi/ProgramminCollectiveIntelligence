import feedparser
import re

#返回一个RSS订阅源的标题和包含单词计数情况的字典
#
def getwordcounts(url):
	#解析订阅源
	d = feedparser.parse(url)
	wc = {}

	#循环遍历所有的文章条目
	#
	for e in d.entries:
		if 'summary' in e:
			summary = e.summary
		else:
			summary = e.description

		#提取一个单词列表
		words = getwords(e.title + ' ' + summary)
		for word in words:
			wc.setdefault(word, 0)
			wc[word] += 1

	return d.feed.title, wc

def getwords(html):
	#去除所有的html标记
	txt = re.compile(r'<[^>]+>').sub('', html)

	#利用所有非字典字母字符拆分出单词
	words = re.compile(r'[^A-Z^a-z]+').split(txt)

	#转化成小写形式
	return [word.lower() for word in words if word != '']


apcount = {}
wordcounts = {}
file = open('feedlist.txt', 'r').read()
feedlist = [line for line in file]
for feedurl in feedlist:
	title, wc = getwordcounts(feedurl)
	wordcounts[title] = wc
	for word, count in wc.items():
		apcount.setdefault(word, 0)
		if count > 1:
			apcount[word] += 1

print(apcount)