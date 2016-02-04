Welcome to the EUROBOT project!
===============================

The aim of this project is to automate the production of songs within the
Eurobeat genre. This will save Eurobeat artists roughly 2000 hours of work per
year, without any noticeable drop in song quality.

Dependencies
-------------
This project depends on [Beautiful Soup 4][1], [Requests][2] and the [Natural Language Toolkit][3]
To install all dependencies, simply type into a terminal:
`pip install beautifulsoup4 requests nltk`

Individual components within the project:
-----------------------------------------
### main.py
Runs all of the modules below in sequential order. This will generate a new song
if everything goes well.

### LyricScraper
LyricScraper scrapes the eurobeat-prime.com lyrics database and stores
information in SongData objects. A list of all SongData objects is returned for
further processing. If the module is called in a stand-along fashion, then the
array gets pickled with the default python pickling library and stored to
songs.pkl.

### LyricParse
LyricParse deals with measuring the frequency of grammar components of the input
songs. It measures the number of paragraphs, lines per paragraph and words per
line in each song. Also, it determines the frequency of a given part of speech 
following another, the frequency of a part of speech starting a line, and the
frequency of a word being a specific part of speech. If this module is run alone
then these results are stored in grammar.pkl.

### LyricGenerate
LyricGenerate takes the previously generated grammar object and uses it to
create the lyrics of a new song. It randomly samples multiple distributions to
do so. The distributions determine number of paragraphs, lines, and words as
well as what part of speech and what word to include in the song. This doesn't 
produce a very good result, and will require further work to produce acceptable
lyrics. 

### Other Files
Other files are documented in their docstrings.

[1]: http://www.crummy.com/software/BeautifulSoup/
[2]: http://docs.python-requests.org/
[3]: http://www.nltk.org/
