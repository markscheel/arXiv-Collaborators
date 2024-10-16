# arXiv Collaborators

A simple script for getting a list of an author's collaborators and a count of
how many papers on which they have collaborated, based on information from
arXiv.org. This is useful for NSF proposals.

## Setup
Requires [feedparser](https://pypi.python.org/pypi/feedparser) which can be
installed with
```
pip install -r requirements.txt
```

## Usage
Run with
```
python arxiv-collaborators.py --arxiv-name Deppe_N --years 4 --formatting NsfProposal > ForNsf.csv
```
The output is printed to screen, so I recommend streaming to a CSV or TSV file.

Note that authors that do not have an affiliation are printed to terminal
(stderr) so that you know who to add affiliations for.

In the script there are two dictionaries. `remapped_names` is for dealing with
authors who have multiple names on the arxiv. `affiliations` is for associating
people with institutions. These will be dependent on your use-case and could
easily be factored out into a separate file for added flexibility.
