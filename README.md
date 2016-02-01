Welcome to the EUROBOT project!
===============================

The aim of this project is to automate the production of songs within the
Eurobeat genre. This will save Eurobeat artists roughly 2000 hours of work per
year, without any noticeable drop in song quality.

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
