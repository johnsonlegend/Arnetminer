# Arnetminer
Data Crawling for person and paper information on AMiner. \
With a input file specifying a list of person's name (and affiliation), it can collect information from AMiner as following: \
* Person: name, #Papers, #Citations, h-index, G-index, Publication over years. 
* Paper: Title, Citations, Publication date, All authors (and affiliation for each person), Venue name. \
The result is stored in json format, a sample entry would be:
```
{'#Citations': '60', 
'#Papers': '2', 
'G-index': '2',
'Paper': [{'Author': [{'Affiliation': 'Lehigh University',
    'Name': 'Madalene Spezialetti'},
   {'Affiliation': 'University of Pittsburgh', 'Name': 'Rajiv Gupta'}],
  'Citations': 14,
  'Publication date': 1994,
  'Title': 'Perturbation Analysis: A Static Analysis Approach for the Non-Intrusive Monitoring of Distributed Programs',
  'Venue Name': 'ICPP'},
 {'Author': [{'Affiliation': 'University of Pittsburgh', 'Name': 'Chun Gong'},
   {'Affiliation': 'University of Pittsburgh', 'Name': 'Rajiv Gupta'},
   {'Affiliation': 'University of Pittsburgh', 'Name': 'Rami G. Melhem'}],
  'Citations': 46,
  'Publication date': 1993,
  'Title': 'Compilation Techniques for Optimizing Communication on Distributed-Memory Systems',
  'Venue Name': 'ICPP'}],
'Publication over years': "[{'year': 1994, 'size': 1}, {'year': 1993, 'size': 1}]",
'h-index': '2',
'name': 'Rajiv Gupta'}
```

# Prerequisite
Phantomjs 2.1.1 \
Selenium 3.4.3

# Installment
Download Phantomjs from [Phantomjs.org](http://phantomjs.org/download.html). Add the excutable phantomjs.exe to PATH. \
`Pip install -U (--user) selenium`

# Usage
python crawler.py

# Default Config
INPUT_FILE: test.txt \
OUTPUT_FILE: result.txt \
Optional: affiliation.txt person_failed.txt person_not_found.txt

# Suggestion
Run the crawler on server. \
Use proxy. 
