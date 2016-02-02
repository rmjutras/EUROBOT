#! /usr/bin/env python3
''' Provides functions to parse a set of lyrics'''

import pickle

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
    
def lines_per_paragraph(song_data):
    ''' Returns a list with the count of lines in each paragraph '''
    nested = generate_nested(song_data)
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
    
if __name__ == "__main__":
    ''' Parses lyrics in pickled.bin and provides analysis data.'''
    pickle_file = open('pickled.bin','rb')
    song_objects = pickle.load(pickle_file)
    pickle_file.close()
        
    line_counts = []
    paragraph_counts = []
    
    for song in song_objects:
        line_count = lines_per_paragraph(song)
        paragraph_counts.append(len(line_count))
        line_counts += line_count
        
    import numpy as np
    import matplotlib.pyplot as plt
    
    plt.hist(line_counts, 16, (0,16))
    plt.xlabel("Lines per Paragraph")
    plt.ylabel("Frequency")
    plt.title("Frequency of lines per paragraph")
    plt.figure()
    
    plt.hist(paragraph_counts, 16, (0,16))
    plt.xlabel("Paragraphs per song")
    plt.ylabel("Frequency")
    plt.title("Frequency of paragraphs per song")
    
    nltk_component_check()
    
    pairs = []
    tagset_map = nltk.tagset_mapping('en-ptb', 'universal')
    
    for song in song_objects:
        for paragraph in generate_nested(song):
            for line in paragraph:
                tagged = nltk.pos_tag(nltk.word_tokenize(line))
                tagged = [(tag[0], tagset_map[tag[1]]) for tag in tagged]
                pairs += nltk.bigrams(tagged)
    
    after_noun = [b[1]  for (a, b) in pairs if a[1] == 'NOUN']
    
    plt.bar(np.arange(len(after_noun)), after_noun)
    plt.ylabel("Frequency")
    plt.title("Frequency of parts of speech after a noun")

    plt.show()
    
    
    
