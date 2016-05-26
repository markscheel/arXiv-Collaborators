import feedparser
import os
import datetime
import time

arXiv_url = 'http://export.arxiv.org/api/query?search_query=au:{0}&id_list=&start=0&max_results=10000'

def main():
	author_list = open('Input/Authors.dat', 'r').readlines()

	date_time = datetime.datetime.now().strftime('%Y_%M_%d_%H_%M_%S')

	for author in author_list:
		file_out = open('Output/{0}_{1}.dat'.format(date_time, author.strip()), 'w')
		author_feed = feedparser.parse(arXiv_url.format(author.rstrip()))

		coauthors = {}

		count = 0		
		total = len(author_feed.entries)
		for author_paper in author_feed.entries:
			count += 1
			print('{0}/{1}: {2}'.format(count, total, author_paper.title))
		
			for coauthor in author_paper.authors:
		 		try:
		 			coauthors[coauthor.name] += 1
		 		except KeyError:
		 			coauthors[coauthor.name] = 1
		for c in coauthors:
			print('{0}, {1}'.format(c, coauthors[c]), file=file_out)

	time.sleep(3)

if __name__ == '__main__':
	main()