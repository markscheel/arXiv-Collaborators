# arXiv Collaborators

A simple script for getting a list of an author's collaborators and a count of how many papers on which they have collaborated, based on information from arXiv.org.

## Setup
Requires [feedparser](https://pypi.python.org/pypi/feedparser) which can be installed with 
``` 
pip install -r requirements.txt
```

## Usage
Place the authors to query into `Input/Authors.dat`, formatted as they appear when searching in arXiv, for example Joseph Polchinski is formatted as `Polchinski_J`.

Run with 
```
python arxiv-collaborators.py
```

Output is placed in the `Output/` directory and named with the current date/time and the author's name. One output file is generated for each author.