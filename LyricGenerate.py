#! /usr/bin/env python3
''' Generates lyrics from a grammar object'''

import random

from WeightedList import WeightedList

def select(counter):
    weighted = WeightedList(counter)
    return random.choice(weighted)

def generate_song(grammar):
    num_paras = select(grammar['song_paragraphs'])
    song = []
    for para in range(num_paras):
        num_lines = select(grammar['paragraph_lines'])
        paragraph = []
        for line in range(num_lines):
            line = []
            num_words = select(grammar['line_words'])
            for word_num in range(num_words):
                if word_num == 0:
                    part_of_speech = select(grammar['line_starts'])
                else:   
                    part_of_speech = select(
                            grammar['after_pos'][line[word_num-1][1]])
                    
                correct_case = False
                while not correct_case:
                    word = select(grammar['common_words'][part_of_speech])
                    if word[0].isupper() and word_num == 0:
                        correct_case = True
                    elif word[0].islower() and word_num > 0:
                        correct_case = True
                    
                line.append((word, part_of_speech))
            paragraph.append(line)
        song.append(paragraph)
    
    return song

if __name__ == '__main__':
    import pickle
    pickle_file = open('grammar.pkl','rb')
    grammar = pickle.load(pickle_file)
    pickle_file.close()
    
    song = generate_song(grammar)
    
    for para in song:
        for line in para:
            print(' '.join([w for (w,p) in line]))
        print()
    print()
    
    
