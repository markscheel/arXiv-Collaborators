import time
from datetime import datetime as dt
from collections import defaultdict

import feedparser as fp

arXiv_url = 'http://export.arxiv.org/api/query?search_query=au:{0}&id_list=&start=0&max_results=10000'
input_path = 'Input'
output_path = 'Output'


def main():
	author_list = open(f'{input_path}/Authors.dat', 'r').readlines()

	date_time = dt.now().strftime('%Y_%M_%d_%H_%M_%S')

	for author in author_list:
		# Get the data from arXiv
		author = author.strip()
		feed = fp.parse(arXiv_url.format(author))

		# Create an empty dict to store counts of the coauthors
		coauthors = defaultdict(int)

		total = len(feed.entries)

		for i, paper in enumerate(feed.entries):
			title = paper.title.encode('utf-8')
			print(f'{i + 1}/{total}: {title}')

			for coauthor in paper.authors:
	 			coauthors[coauthor.name] += 1

		# Open a unique file for this author
		f_name = f'{output_path}/{date_time}_{author}.dat'
		with open(f_name, 'w') as fp_out:
			for name, count in coauthors.items():
				print(f'{name}, {count}', file=fp_out)

	# Limit the query rate to be nice to the arXiv servers.
	time.sleep(3)


if __name__ == '__main__':
	main()
