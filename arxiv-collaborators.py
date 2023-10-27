#!/bin/env python

import time
from datetime import datetime as dt
import feedparser as fp
from enum import Enum

remapped_names = {
    "Tom Wlodarczyk": "Tom Włodarczyk",
    "Francois Hebert": "François Hébert",
    "Nils Vu": "Nils L. Vu",
    "Nils Fischer": "Nils L. Vu",
    "Nils L. Fischer": "Nils L. Vu",
    "Gabriel S. Bonilla": "Marceline S. Bonilla",
    "Nils Deppe": "Deppe_N",
}

affiliations = {
    "Aaron B. Zimmerman": "UT Austin",
    "Adam Pound": "University of Southampton",
    "Andrea Ceja": "Cal State Fullerton",
    "Antoni Ramos-Buades": "Albert Einstein Institute",
    "Arnab Bhani": "Penn State",
    "Bela Szilagyi": "Caltech",
    "Charles J. Woodford": "University of Toronto",
    "Cristobal Armaza": "Cornell University",
    "Daniel Vieira": "Cornell University",
    "David Vartanyan": "UC Berkeley",
    "Davide Gerosa": "Universitá degli Studi di Milano-Bicocca",
    "Eamonn O'Shea": "Cornell University",
    "Francois Foucart": "University of New Hampshire",
    "Hannes R. Rüter": "University of Coimbra",
    "Harald P. Pfeiffer": "Albert Einstein Institute",
    "Himanshu Chaudhary": "Caltech",
    "Isha Anantpurkar": "UCSB",
    "Jason S. Guo": "Cornell University",
    "Daniel Hemberger": "NASA JPL",
    "Ian Hinder": "Albert Einstein Institute",
    "Tanja Hinderer": "Utrecht University",
    "Peter James Nee": "Albert Einstein Institute",
    "Andrew R. Frey": "University of Winnipeg",
    "Alyssa Garcia": "Cal State Fullerton",
    "Kuo-Chuan Pan": "National Tsing Hua University",
    "Ling Sun": "The Australian National University",
    "Max Miller": "University of New Hampshire",
    "Evan Foley": "Cal State Fullerton",
    "Nicholas Demos": "Cal State Fullerton",
    "Heather Fong": "University of Tokyo",
    "Brad Cownden": "Jagiellonian University",
    "Nicholas Demos": "MIT",
    "Arnab Dhani": "Penn State University",
    "Nousha Afshari": "Cal State Fullerton",
    "Jennifer Sanchez": "Cal State Fullerton",
    "Jonathan Blackman": "Caltech",
    "Qingwen Wang": "Perimeter Institute",
    "Steven J. VanCamp": "Michigan State University",
    "Jooheon Yoo": "Cornell University",
    "Jordan Moxon": "Caltech",
    "Katerina Chatziioannou": "Caltech",
    "Keefe Mitman": "Caltech",
    "Kevin Barkett": "Caltech",
    "Kyle C. Nelli": "Caltech",
    "Lam Hui": "Columbia University",
    "Leo C. Stein": "University of Mississippi",
    "Leor Barack": "University of Southampton",
    "Lorena Magaña Zertuche": "University of Mississippi",
    "Alexander Chernoglazov": "University of Maryland",
    "François Hébert": "JCSDA",
    "Dante A. B. Iozzo": "Cornell University",
    "Reza Katebi": "Cal State Fullerton",
    "Haroon Khan": "Cal State Fullerton",
    "Neev Khera": "Penn State University",
    "Lawrence E. Kidder": "Cornell University",
    "Yoonsoo Kim": "Caltech",
    "Prayush Kumar": "Tata Institute of Fundamental Research",
    "Kevin Kuper": "Cal State Fullerton",
    "Macarena Lagos": "Columbia University",
    "Guillermo Lara": "Albert Einstein Institute",
    "Isaac Legred": "Caltech",
    "Dongjun Li": "Caltech",
    "Halston Lim": "MIT",
    "Oliver Long": "Albert Einstein Institute",
    "Tommaso De Lorenzo": "Cornell University",
    "Geoffrey Lovelace": "Cal State Fullerton",
    "Sizheng Ma": "Perimeter Institute",
    "Alexandra Macedo": "Cal State Fullerton",
    "Denyz Melchor": "UCLA",
    "Marceline S. Bonilla": "Cal State Fullerton",
    "Maria Okounkova": "Pasadena City College",
    "Marissa Walker": "Christopher Newport University",
    "Mark A. Scheel": "Caltech",
    "Marlo Morales": "Washington State University",
    "Matteo Boschini": "Albert Einstein Institute",
    "Matthew D. Duez": "Washington State University",
    "Matthew Giesler": "Cornell University",
    "Mekhi Dhesi": "University of Southampton",
    "Michael A. Pajkos": "Caltech",
    "Michael Boyle": "Cornell University",
    "Nikolas A. Wittek": "Albert Einstein Institute",
    "Nils L. Vu": "Caltech",
    "Patricia Schmidt": "University of Birmingham",
    "Peter J. Nee": "Albert Einstein Institute",
    "Samuel Rodriguez": "Cal State Fullerton",
    "Saul A. Teukolsky": "Cornell University",
    "Scott E. Field": "University of Massachusetts Dartmouth",
    "Sean M. Couch": "Michigan State University",
    "Serguei Ossokine": "Albert Einstein Institute",
    "Sierra Thomas": "Syracuse University",
    "Teresita Ramirez": "Northwestern",
    "Tom Włodarczyk": "Albert Einstein Institute",
    "Tony Chu": "Princeton",
    "Vijay Varma": "University of Massachusetts Dartmouth",
    "William Throwe": "Cornell University",
    "Yitian Chen": "Cornell University",
}


class Format(Enum):
    NsfAccess = 1
    NsfProposal = 2


def get_initials(name):
    """Take a name, First Middles Last -> F. M. Last
    """
    split_name = name.strip().split()
    initial_name = ""
    for i in range(len(split_name) - 1):
        initial_name += split_name[i][0].upper() + '. '
    return initial_name + split_name[-1]  # add last name


def get_last_name_first(name):
    """Take a name, First Middle Last -> Last First M.
    """
    split_name = name.strip().split()
    initial_name = str(split_name[0]) + " "
    for i in range(1, len(split_name) - 1):
        initial_name += split_name[i][0].upper() + '. '
    return split_name[-1] + ", " + initial_name  # add last name


def print_authors(author,
                  years_back,
                  formatting,
                  show_papers=False,
                  show_skipped=False):
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
        month_updated = paper.updated_parsed.tm_mon
        day_updated = paper.updated_parsed.tm_mday
        link = paper.link

        if year_updated + years_back < current_year:
            if show_skipped:
                print(f'{i + 1}/{total_papers}: {year_updated} '
                      f'{title}--Skipping ')
            continue

        if show_papers:
            print(f'{i + 1}/{total_papers}: {year_updated} {title}')

        for coauthor in paper.authors:
            name = coauthor.name
            # Remap names to the same spelling
            if name in remapped_names:
                name = remapped_names[name]

            if name == author:
                continue

            coauthor_name = get_initials(name)
            if coauthor_name in coauthors:
                count = coauthors[coauthor_name][0] + 1
                if coauthors[coauthor_name][1] > year_updated:
                    coauthors[coauthor_name] = [
                        count, coauthors[coauthor_name][1],
                        coauthors[coauthor_name][2],
                        coauthors[coauthor_name][3],
                        coauthors[coauthor_name][4],
                        coauthors[coauthor_name][5]
                    ]
                else:
                    coauthors[coauthor_name] = [
                        count, year_updated, month_updated, day_updated, link,
                        name
                    ]
            else:
                coauthors[coauthor_name] = [
                    1, year_updated, month_updated, day_updated, link, name
                ]

    longest_name_length = max(coauthors.keys())
    if formatting == Format['NsfAccess']:
        print("Name | Number of Papers | Last Paper")
        for name in sorted(coauthors, key=lambda x: x.split()[-1]):
            print(f'{name.replace(". ", ".~"):30} '
                  f'{coauthors[name][1]} {coauthors[name][0]:4} '
                  f'{coauthors[name][2]}')
    elif formatting == Format['NsfProposal']:
        print("Name")
        for name in sorted(coauthors, key=lambda x: x.split()[-1]):
            to_print = str(
                f'{get_last_name_first(coauthors[name][5])}').strip()
            if coauthors[name][5] in affiliations:
                to_print += f'\t{affiliations[coauthors[name][5]]}'
            to_print += f'\t\t{coauthors[name][2]}/{coauthors[name][3]}/{coauthors[name][1]}'
            print(to_print)


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
    parser.add_argument('--formatting',
                        help='The format to output the authors in.',
                        choices=['NsfAccess', 'NsfProposal'],
                        required=True)
    args = parser.parse_args()
    formatting = Format[args.formatting]
    print_authors(args.arxiv_name, args.years, formatting)
