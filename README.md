Welcome to the EUROBOT project!
===============================

The aim of this project is to automate the production of songs within the
Eurobeat genre. This will save Eurobeat artists roughly 2000 hours of work per
year, without any noticeable drop in song quality.

Dependencies
-------------
This project depends on [Beautiful Soup 4][1] and the [Natural Language Toolkit][2]
To install all dependencies, simply type into a terminal:
`pip install bs4 nltk`

Individual components within the project:
-----------------------------------------

### LyricScraper
LyricScraper is a stand-alone python file which scrapes the eurobeat-prime.com
lyrics database and stores the lyrics to lyrics.txt. Also the SongData objects 
for each song gets pickled with the default python pickling library and stored
to pickled.bin. This is the only way to recover the artist and title
information.

### Other Files
Other files are documented in their docstrings.

[1]: http://www.crummy.com/software/BeautifulSoup/
[2]: http://www.nltk.org/
