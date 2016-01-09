#! /usr/bin/python3
''' Scrapes the lyrics from the eurobeat-prime.com database.'''

from SongData import SongData
from bs4 import BeautifulSoup
import urllib.request as request
import sys
import multiprocessing

def get_song_urls():
    ''' Reads the urls for all of the songs in the database.'''
    SONG_URL = 'http://www.eurobeat-prime.com/lyrics.php'
    ARTIST_URL = 'http://www.eurobeat-prime.com/lyrics.php?artist='
    ARTIST_OPTIONS = '1abcdefghijklmnopqrstuvwxyz'
    
    song_urls = []
    for option in ARTIST_OPTIONS:
        artist_page = request.urlopen(ARTIST_URL + option)
        soup = BeautifulSoup(artist_page.readall(), 'html.parser')
        
        song_links = soup.find('div', class_='mmids').find_all("a")
        song_urls += [SONG_URL + link.get("href") for link in song_links]
        
    return song_urls
      
def parallel_scrape_songs(urllist):
    ''' Scrapes the lyrics of a each song in a list of urls. Uses parallel threads.'''
    pool = multiprocessing.Pool(8)
    scrape_data = []
    max_i = 0
    count = len(urllist)
    for i, data in enumerate(pool.imap_unordered(scrape_song, urllist), 1):
        max_i = max(i, max_i)
        if i%2 == 0:
            short_artist = data.artist[:19] + ".." if 
                    len(data.artist) > 21 else data.artist
            title_length = 66 - len(short_artist)
            short_title = data.title[:title_length] + ".." if \
                    len(data.title) > title_length else data.title
            out_string = short_artist + " - " + short_title
            print("\r{:8.2f}% {:69s}".format(max_i/count*100, out_string), end='')
        scrape_data.append(data)
    return scrape_data

def scrape_songs(urllist):
    ''' Scrapes the lyrics of a each song in a list of urls.'''
    scrape_data = []
    count = len(urllist)
    for i, url in enumerate(urllist, 1):
        result = scrape_song(url)
        scrape_data.append(result)
    return scrape_data
    
def scrape_song(url):
    ''' Scrapes the lyrics of a single song.'''
    song_page = request.urlopen(url)
    song_soup = BeautifulSoup(song_page.readall(), 'html.parser')
    
    lyrics_box = song_soup.find('div', class_='mmids')
    artist_title = lyrics_box.b.extract().text
    artist = artist_title.split('-')[0].strip()
    title = artist_title.split('-')[1].strip()
    lyrics = lyrics_box.text.strip() + "\n"

    return SongData(artist, title, lyrics)

if __name__ == "__main__":
    print("Loading list of songs to scrape...")
    urls = get_song_urls()
    print("    {:d} songs found.".format(len(urls)))
    print("Scraping songs...")
    results = parallel_scrape_songs(urls)
    lyric_dump = open('lyrics.txt',encoding='utf-8', mode='w')
    lyric_dump.writelines("\n".join([data.lyrics for data in results]))
    lyric_dump.close()
    
    import pickle
    pickle_file = open('pickled.bin','wb')
    pickle.dump(results, pickle_file)
    pickle_file.close()
    
