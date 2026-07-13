#!/bin/env python

import time
from datetime import datetime as dt
import feedparser as fp
from enum import Enum
import sys

remapped_names = {
    "Béla Szilágyi": "Bela Szilagyi",
    "Cristóbal Armaza": "Cristobal Armaza",
    "Daniel A. Hemberger": "Daniel Hemberger",
    "Francois Hebert": "François Hébert",
    "Gabriel S. Bonilla": "Marceline S. Bonilla",
    "Hannes Rüter": "Hannes R. Rüter",
    "Harald Pfeiffer": "Harald P. Pfeiffer",
    "Isabella Pretto": "Isabella G. Pretto",
    "Larry Kidder": "Lawrence E. Kidder",
    "Mark A Scheel": "Mark A. Scheel",
    "Matthew Duez": "Matthew D. Duez",
    "Nils Deppe": "Deppe_Nils",
    "Nils Fischer": "Nils L. Vu",
    "Nils L. Fischer": "Nils L. Vu",
    "Nils Vu": "Nils L. Vu",
    "Saul Teukolsky": "Saul A. Teukolsky",
    "Tom Wlodarczyk": "Tom Włodarczyk",
}

affiliations = {
    "Aaron B. Zimmerman": "UT Austin",
    "Abhishek Ravishankar": "University of Massachusetts Dartmouth",
    "Adam Pound": "University of Southampton",
    "Adhrit Ravichandran": "University of Massachusetts Dartmouth",
    "Alessandro Nagar": "INFN Sezione di Torino",
    "Alexander Carpenter": "Cal State Fullerton",
    "Alexander Chernoglazov": "University of Maryland",
    "Alexandra Macedo": "Cal State Fullerton",
    "Alyssa Garcia": "Cal State Fullerton",
    "Andrea Ceja": "Cal State Fullerton",
    "Andrew R. Frey": "University of Winnipeg",
    "Aniket Khairnar": "University of Mississippi",
    "Anıl Zenginoğlu": "University of Maryland",
    "Antoni Ramos-Buades": "University of the Balearic Islands",
    "Arnab Dhani": "Penn State University",
    "Azer Afram": "Cal State Fullerton",
    "Bela Szilagyi": "Caltech",
    "Brad Cownden": "Jagiellonian University",
    "C. Melize Ferrus": "King's College London:",
    "Charles J. Woodford": "University of Toronto",
    "Cristobal Armaza": "Cornell University",
    "Daniel Hemberger": "NASA JPL",
    "Daniel Tellez": "Cal State Fullerton",
    "Daniel Vieira": "Cornell University",
    "Dante A. B. Iozzo": "Cornell University",
    "David Maibach": "University of Heidelberg",
    "David Vartanyan": "University of Idaho",
    "Davide Gerosa": "Universitá degli Studi di Milano-Bicocca",
    "Denyz Melchor": "UCLA",
    "Dongjun Li": "University of Illinois Urbana-Champaign",
    "Dongze Sun": "Caltech",
    "Eamonn O'Shea": "Cornell University",
    "Elias R. Most": "Caltech",
    "Eric Thrane": "Monash University",
    "Evan Foley": "Cal State Fullerton",
    "Francois Foucart": "University of New Hampshire",
    "Frans Pretorius": "Princeton University",
    "François Hébert": "JCSDA",
    "Geoffrey Lovelace": "Cal State Fullerton",
    "Gregorio Carullo": "University of Birmingham",
    "Gregory B. Cook": "Wake Forest University",
    "Guillermo Lara": "Albert Einstein Institute",
    "Guido Da Re": "Caltech",
    "Halston Lim": "MIT",
    "Hannes R. Rüter": "University of Coimbra",
    "Harald P. Pfeiffer": "Albert Einstein Institute",
    "Haroon Khan": "Cal State Fullerton",
    "Harrison Siegel": "Columbia University & Flatiron Institute",
    "Heather Fong": "University of Tokyo",
    "Hengrui Zhu": "Princeton University",
    "Henri Inchauspé": "KU Leuven",
    "Himanshu Chaudhary": "Caltech",
    "Iago B. Mendes": "Oberlin College",
    "Ian Hinder": "Albert Einstein Institute",
    "Isaac Legred": "University of Illinois Urbana-Champaign",
    "Isabella G. Pretto": "Caltech",
    "Isha Anantpurkar": "UCSB",
    "Jason S. Guo": "Cornell University",
    "Jennifer Sanchez": "Cal State Fullerton",
    "Jiaxi Wu": "Caltech",
    "Jonathan Blackman": "Caltech",
    "Jooheon Yoo": "Cornell University",
    "Jordan Moxon": "Caltech",
    "Justin L. Ripley": "Johns Hopkins University",
    "Károly Zoltán Csukás": " Magyar Tudományos Akadémia Wigner Fizikai Kutatóközpont Részecske-és Magfizikai Intézet",
    "Katerina Chatziioannou": "Caltech",
    "Katie Rink": "UT Austin",
    "Keefe Mitman": "Caltech",
    "Ken Z. Jones": "Cal State Fullerton",
    "Kevin Barkett": "Caltech",
    "Kevin Kuper": "Cal State Fullerton",
    "Kuo-Chuan Pan": "National Tsing Hua University",
    "Kyle C. Nelli": "Caltech",
    "Kyle Pannone": "Cal State Fullerton",
    "Lam Hui": "Columbia University",
    "Lavinia Heisenberg": "University of Heidelberg",
    "Lawrence E. Kidder": "Cornell University",
    "Leda Gao": "Wake Forest University",
    "Leo C. Stein": "University of Mississippi",
    "Leor Barack": "University of Southampton",
    "Ling Sun": "The Australian National University",
    "Lorena Magaña Zertuche": "Niels Bohr Institute",
    "Luisa T. Buchman": "Washington State University, Pullman",
    "Macarena Lagos": "Columbia University",
    "Marceline S. Bonilla": "College of Marin",
    "Maria Okounkova": "Pasadena City College",
    "Marina De Amicis": "Perimeter Institute for Theoretical Physics",
    "Marissa Walker": "Christopher Newport University",
    "Mark A. Scheel": "Caltech",
    "Marlo Morales": "Washington State University",
    "Matteo Boschini": "Albert Einstein Institute",
    "Matthew D. Duez": "Washington State University",
    "Matthew Giesler": "Cornell University",
    "Max Miller": "University of New Hampshire",
    "Maxence Corman": "Albert Einstein Institute",
    "Maximiliano Isi": "Flatiron Institute",
    "Md Arif Shaikh": "Vidyasagar University",
    "Mekhi Dhesi": "University of Southampton",
    "Michael A. Pajkos": "Caltech",
    "Michael Boyle": "Cornell University",
    "Naritaka Oshita": "Kyoto University",
    "Neev Khera": "Penn State University",
    "Nicholas Demos": "Cal State Fullerton",
    "Nicholas Demos": "MIT",
    "Nicholas J. Corso": "Cornell University",
    "Nikolas A. Wittek": "Albert Einstein Institute",
    "Nils L. Vu": "Caltech",
    "Noora Ghadiri": "University of Illinois Urbana-Champaign",
    "Nousha Afshari": "Cal State Fullerton",
    "Oliver Long": "Albert Einstein Institute",
    "Patricia Schmidt": "University of Birmingham",
    "Paul D. Lasky": "Monash University",
    "Peter J. Nee": "Albert Einstein Institute",
    "Peter James Nee": "Albert Einstein Institute",
    "Prayush Kumar": "Tata Institute of Fundamental Research",
    "Qingwen Wang": "Perimeter Institute",
    "Reza Katebi": "Cal State Fullerton",
    "Robert Owen": "Oberlin College",
    "Samuel Rodriguez": "Cal State Fullerton",
    "Sarah Habib": "Caltech",
    "Saul A. Teukolsky": "Cornell University",
    "Scott E. Field": "University of Massachusetts Dartmouth",
    "Sean M. Couch": "Michigan State University",
    "Sebastiano Bernuzzi": "Friedrich Schiller University in Jena",
    "Serguei Ossokine": "Albert Einstein Institute",
    "Sierra Thomas": "Syracuse University",
    "Simone Albanesi": "Friedrich Schiller University in Jena",
    "Sizheng Ma": "Perimeter Institute",
    "Steven J. VanCamp": "Michigan State University",
    "Tanja Hinderer": "Utrecht University",
    "Taylor Knapp": "Caltech",
    "Teagan A. Clarke": "Monash University",
    "Teresita Ramirez": "Northwestern",
    "Teresita Ramirez-Aguilar": "Northwestern University",
    "Tom Włodarczyk": "Albert Einstein Institute",
    "Tommaso De Lorenzo": "Cornell University",
    "Tony Chu": "Princeton University",
    "Tousif Islam": "Kavli Institute for Theoretical Physics, University of California Santa Barbara",
    "Vijay Varma": "University of Massachusetts Dartmouth",
    "Vitor Cardoso": "Niels Bohr Institute & Técnico",
    "Will M. Farr": "Flatiron Institute & Stony Brook University",
    "William Throwe": "Cornell University",
    "Yitian Chen": "Cornell University",
    "Yoonsoo Kim": "Caltech",
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
            else:
                print(f"Could find an affiliation for {coauthors[name][5]}", file=sys.stderr)
            to_print += f'\t\t{coauthors[name][2]}/{coauthors[name][3]}/{coauthors[name][1]}'
            print(to_print)


if __name__ == '__main__':
    import argparse as ap
    parser = ap.ArgumentParser(
        prog='arxiv-collaborators',
        description='Pull list of arxiv collaborators based on your arxiv name.'
    )
    parser.add_argument('--arxiv-name',
                        help='Your arxiv name, e.g. Deppe_Nils',
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
