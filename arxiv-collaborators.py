import feedparser as fp
from datetime import datetime as dt
import time

arXiv_url = 'http://export.arxiv.org/api/query?search_query=au:{0}&id_list=&start=0&max_results=10000'

def main():
	author_list = open('Input/Authors.dat', 'r').readlines()

	date_time = dt.now().strftime('%Y_%M_%d_%H_%M_%S')

	for author in author_list:

		# Open a unique file for this author
		file_out = open('Output/{0}_{1}.dat'.format(date_time, author.strip()), 'w')

		# Get the data from arXiv
		author_feed = fp.parse(arXiv_url.format(author.rstrip()))

		# Create an empty dict to store counts of the coauthors
		coauthors = {}

		count = 0
		total = len(author_feed.entries)

		for author_paper in author_feed.entries:

			# Print out which paper we're up to so we can keep track as its running.
			count += 1
			print('{0}/{1}: {2}'.format(count, total, author_paper.title.encode('utf-8')))

			for coauthor in author_paper.authors:
		 		# Try to increase the count in the dict, if an exception is
		 		# raised the key must not exist yet, so create it.
		 		try:
		 			coauthors[coauthor.name] += 1
		 		except KeyError:
		 			coauthors[coauthor.name] = 1

		# Iterate over the dict and write the information to file.
		for c in coauthors:
			print('{0}, {1}'.format(c, coauthors[c]), file=file_out)

		file_out.close()

	# Limit the query rate to be nice to the arXiv servers.
	time.sleep(3)

if __name__ == '__main__':
	main()
