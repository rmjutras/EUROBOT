#!/usr/bin/env python3
''' Scrapes the lyrics from the eurobeat-prime.com database.'''

from __future__ import print_function, division
import sys
import time
import multiprocessing
import requests
from requests.exceptions import ConnectionError

from bs4 import BeautifulSoup
from SongData import SongData

# Keeps the connection alive instead of reconnecting constantly
session = requests.Session()

def get_song_urls():
    ''' Reads the urls for all of the songs in the database.'''
    SONG_URL = 'http://www.eurobeat-prime.com/lyrics.php'
    ARTIST_URL = 'http://www.eurobeat-prime.com/lyrics.php?artist='
    ARTIST_OPTIONS = '1abcdefghijklmnopqrstuvwxyz'
    
    song_urls = []
    for option in ARTIST_OPTIONS:
        artist_page = session.get(ARTIST_URL + option)
        soup = BeautifulSoup(artist_page.text, 'html.parser')
        
        song_links = soup.find('div', class_='mmids').find_all("a")
        song_urls += [SONG_URL + link.get("href") for link in song_links]
        
    return song_urls
      
def parallel_scrape_songs(urllist):
    ''' Scrapes the lyrics of a each song in a list of urls.
        Uses parallel threads.'''
    pool = multiprocessing.Pool(16)
    scrape_data = []
    count = len(urllist)
    for i, data in enumerate(pool.imap_unordered(scrape_song, urllist), 1):
        if i%10 == 0:
            short_artist = data.artist[:19] + ".." if \
                    len(data.artist) > 21 else data.artist
            title_length = 66 - len(short_artist)
            short_title = data.title[:title_length] + ".." if \
                    len(data.title) > title_length else data.title
            out_string = short_artist + " - " + short_title
            print("\r{:8.2f}% {:69s}".format(i/count*100, out_string), end='')
        scrape_data.append(data)
    print("\r{:8.2f}% Done!{:64s}".format(100,''))
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
    retries = 5
    song_page = None
    while song_page is None or song_page.status_code != requests.codes.ok:
        try:
            song_page = session.get(url)
        except ConnectionError:
            if retries > 0:
                retries -= 1
                time.sleep(1)
            else:
                raise
            
    song_soup = BeautifulSoup(song_page.text, 'html.parser')
    
    lyrics_box = song_soup.find('div', class_='mmids')
    artist_title = lyrics_box.b.extract().text
    artist = artist_title.split('-')[0].strip()
    title = artist_title.split('-')[1].strip()
    lyrics = lyrics_box.text.strip() + "\n"

    return SongData(artist, title, lyrics)

def do_scrape():
    print("Loading list of songs to scrape...")
    urls = get_song_urls()
    print("    {:d} songs found.".format(len(urls)))
    print("Scraping songs...")
    results = parallel_scrape_songs(urls)
    return results
    
if __name__ == "__main__":
    songs = do_scrape()
    
    import pickle
    pickle_file = open('songs.pkl','wb')
    pickle.dump(songs, pickle_file)
    pickle_file.close()
    
