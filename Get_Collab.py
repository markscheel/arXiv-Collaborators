import feedparser
import os
import datetime
import time

def main():
	filename = 'Authors'

	arXiv_url = 'http://export.arxiv.org/api/query?search_query=au:AUTHOR&id_list=&start=0&max_results=10000'

	if os.path.exists(filename + '_Out.txt'): os.remove(filename + '_Out.txt')

	file_in = open('Input/' + filename + '_In.txt', 'r')
	file_out = open('Output/' + filename + '_Out.txt', 'w')

	author_list = file_in.readlines()

	for author in author_list:
		print(author.strip().replace('_', ', '))
		print(author.strip().replace('_', ', '), end = '\n', file = file_out)
		author_feed = feedparser.parse(arXiv_url.replace('AUTHOR', author.rstrip()))

		i = 0
		for author_paper in author_feed.entries:
			i += 1
			count = str(i)
			print(count + ' ' + author_paper.title)
			for coauthor in author_paper.authors:
		 		name = coauthor.name
		 		print(name, end = '\n', file = file_out)
			time.sleep(3)

if __name__ == '__main__':
	main()