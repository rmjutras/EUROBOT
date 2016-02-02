import LyricScraper as ls
import LyricParse as lp

songs = ls.do_scrape()
grammar = lp.do_parse(songs)
