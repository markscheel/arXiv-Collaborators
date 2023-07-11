#!/bin/env python

import time
from datetime import datetime as dt
import feedparser as fp


def get_initials(name):
    """Take a name, First Middles Last -> F. M. Last
    """
    split_name = name.strip().split()
    initial_name = ""
    for i in range(len(split_name) - 1):
        initial_name += split_name[i][0].upper() + '. '
    return initial_name + split_name[-1]  # add last name


def print_authors(author, years_back, show_papers=False, show_skipped=False):
    """gi
    """
    current_year = dt.now().year

    # Get the data from arXiv
    arXiv_url = 'http://export.arxiv.org/api/query?search_query=au:{0}&id_list=&start=0&max_results=10000'
    arxiv_feed = fp.parse(arXiv_url.format(author))

    coauthors = {}
    total_papers = len(arxiv_feed.entries)

    for i, paper in enumerate(arxiv_feed.entries):
        title = paper.title.encode('utf-8')
        # Use last updated to estimate the publish date/year
        year_updated = paper.updated_parsed.tm_year
        link = paper.link

        if year_updated + years_back < current_year:
            if show_skipped:
                print(f'{i + 1}/{total_papers}: {year_updated} '
                      f'{title}--Skipping ')
            continue

        if show_papers:
            print(f'{i + 1}/{total_papers}: {year_updated} {title}')

        for coauthor in paper.authors:
            coauthor_name = get_initials(coauthor.name)
            if coauthor_name in coauthors:
                count = coauthors[coauthor_name][0] + 1
                if coauthors[coauthor_name][1] > year_updated:
                    coauthors[coauthor_name] = [
                        count, coauthors[coauthor_name][1],
                        coauthors[coauthor_name][2]
                    ]
                else:
                    coauthors[coauthor_name] = [count, year_updated, link]
            else:
                coauthors[coauthor_name] = [1, year_updated, link]

    longest_name_length = max(coauthors.keys())
    print("Name | Number of Papers | Last Paper")
    for name in sorted(coauthors, key=lambda x: x.split()[-1]):
        print(f'{name.replace(". ", ".~"):30} '
              f'{coauthors[name][1]} {coauthors[name][0]:4} '
              f'{coauthors[name][2]}')


if __name__ == '__main__':
    import argparse as ap
    parser = ap.ArgumentParser(
        prog='arxiv-collaborators',
        description='Pull list of arxiv collaborators based on your arxiv name.'
    )
    parser.add_argument('--arxiv-name',
                        help='Your arxiv name, e.g. Deppe_N',
                        required=True)
    parser.add_argument(
        '--years',
        help='Number of years back to use for getting collabotars',
        type=int,
        required=True)
    args = parser.parse_args()
    print_authors(args.arxiv_name, args.years)
