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
python arxiv-collaborators.py --arxiv-name Deppe_N --years 4 --formatting NsfProposal > ForNsf.tsv
```
The output is printed to screen, so I recommend streaming to a TSV file.

Note that authors that do not have an affiliation are printed to terminal
(stderr) so that you know who to add affiliations for.

To reduce the chance of missing papers that aren't on the arXiv (or that the
arXiv name search doesn't find), also pass your ORCID:
```
export ADS_TOKEN=...  # from https://ui.adsabs.harvard.edu/user/settings/token
python arxiv-collaborators.py --arxiv-name Deppe_N --years 4 --formatting NsfProposal \
  --orcid 0000-0003-4557-4115 > ForNsf.tsv
```
This additionally queries ADS/SciX (by ORCID, requires `ADS_TOKEN`) and
INSPIRE-HEP (by INSPIRE author ID, looked up from the ORCID or passed with
`--inspire-bai`). Use `--no-ads` or `--no-inspire` to skip a source, or
`--ads`/`--inspire` to make it an error if a source can't be queried (e.g.
`ADS_TOKEN` is not set) instead of just a warning. Papers are matched across sources by arXiv ID, DOI, or title
so each coauthor is counted once per paper. Records found only in ADS/SciX or
INSPIRE, and coauthor names that look like duplicates, are printed to stderr for
review.

With `--orcid`, coauthors missing from the `affiliations` dictionary get the
affiliation listed on their most recent ADS/SciX or INSPIRE record. Curated
institution matches are preferred (ADS canonical affiliations, rolled up from
departments to the institution, and INSPIRE institution records); otherwise
the organization is guessed from the raw affiliation string. Each of these is
printed to stderr with its source paper so you can check it. Note that papers
sometimes list people at a past institution (e.g. large catalog papers list
where the work was done), so the `affiliations` dictionary always takes
precedence. Pass `--check-affiliations` to compare every entry in the
dictionary against the most recent paper, which helps find stale entries.

In the script there are two dictionaries. `remapped_names` is for dealing with
authors who have multiple names on the arxiv. `affiliations` is for associating
people with institutions. These will be dependent on your use-case and could
easily be factored out into a separate file for added flexibility.

## NSF COA Template Excel file
It seems that the NSF website is fairly picky about the exact formatting. As a
result, I've had to use Excel (Office 365 seems to work), but Apple Numbers
doesn't save the Excel file in quite the right format for some reason.
