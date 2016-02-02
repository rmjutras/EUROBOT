#! /usr/bin/env python3
''' Provides functions to parse a set of lyrics'''

from collections import Counter
import multiprocessing

import nltk

from SongData import SongData

def generate_nested(song_data):
    '''Creates a nested list structure from a SongData object.
    Each song becomes a list of paragraphs, and each paragraph is a list of 
    lines of the song. This makes further analysis more simple.
    '''
    result = []
    temp_para = []
    for line in song_data.lyrics.strip().split('\r\n'):
        if '\n' not in line:
            temp_para.append(line)
        else:
            result.append(temp_para)
            temp_para = [line]
    if len(temp_para) > 0:
        result.append(temp_para)
    return result
def lines_per_paragraph(lyrics):
    ''' Returns a list with the count of lines in each paragraph '''
    nested = generate_nested(lyrics)
    lengths = []
    for para in nested:
        lengths.append(len(para))
    return lengths

def nltk_component_check():
    ''' Checks that the required components of the nltk have been downloaded'''
    test = "a bat"
    try:
        nltk.word_tokenize(test)
    except LookupError:
        nltk.download('punkt')
    tokens = nltk.word_tokenize(test)
    try:
        nltk.pos_tag(tokens)
    except LookupError:
        nltk.download('averaged_perceptron_tagger')
    try:
        nltk.tagset_mapping('en-ptb', 'universal')
    except LookupError:
        nltk.download('universal_tagset')
        
# Create a single tagger object to avoid repeated calls to 'load'
nltk_component_check()
tagger = nltk.tag.perceptron.PerceptronTagger()
tagset_map = nltk.tagset_mapping('en-ptb', 'universal')
    
def tag_song(song, simplify=True):
    ''' Returns a nested song structure where each word is tagged with part of
    speech. If 'simplify' is True (default) then all punctuation and special
    words are removed. '''
    
    tagged_song = []
    for paragraph in generate_nested(song):
        tagged_paragraph = []
        for line in paragraph:
            tagged_line = tagger.tag(nltk.word_tokenize(line))
            tagged_line = [(w, tagset_map[p]) for (w, p) in tagged_line if 
                    tagset_map[p] != '.' and tagset_map[p] != 'X']
            tagged_paragraph.append(tagged_line)
        tagged_song.append(tagged_paragraph)
    song.tagged = tagged_song
    return song
            
def do_parse(songs):
    ''' Parses lyrics in songs.pkl and provides analysis data.
    Can be optionally be provided an array with all SongData objects.'''
    
    
    
    after_pos = {} # Frequency of a PoS after another given PoS
    common_words = {} # Frequency of different words for a part of speech
    
    for pos in set(tagset_map.values()):
        if pos != '.' and pos != 'X':
            after_pos[pos] = Counter()
            common_words[pos] = Counter()
            
    line_starts = Counter() # Frequency of a given PoS starting a line of a song
    song_paragraphs = Counter() # Frequency of number of paragraphs per song
    paragraph_lines = Counter() # Frequency of number of lines per paragraph
    line_words = Counter() # Frequency of number of words per line
    
    total = len(songs)
    pool = multiprocessing.Pool()
    
    for i, tagged_song in \
            enumerate(pool.imap_unordered(tag_song, songs), 1):
        if i%16:
            print("\rParsing lyrics...{:6.2f}%".format(i/total*100), end='')
            
        song_paragraphs[len(tagged_song.tagged)] += 1
        
        for paragraph in tagged_song.tagged:
            paragraph_lines[len(paragraph)] += 1
            
            for line in paragraph:
                line_words[len(line)] += 1
                if len(line) > 0:
                    line_starts[line[0][1]] += 1
                    for (w1, w2) in nltk.bigrams(line):
                        after_pos[w1[1]][w2[1]] += 1
                    
    print("\rParsing lyrics...Done!   ")
    return {'after_pos': after_pos, 'common_words': common_words,
            'line_starts': line_starts, 'song_paragraphs': song_paragraphs,
            'paragraph_lines': paragraph_lines, 'line_words': line_words}
    
if __name__ == "__main__":
    import pickle
    pickle_file = open('songs.pkl','rb')
    songs = pickle.load(pickle_file)
    pickle_file.close()
    
    grammar = do_parse(songs)
    
    pickle_file = open('grammar.pkl','wb')
    pickle.dump(grammar, pickle_file)
    pickle_file.close()
