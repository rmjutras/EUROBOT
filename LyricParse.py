def generate_nested(lyrics):
    '''Creates a nested list structure from a lyrics string.
    
    Each song becomes a list of paragraphs, and each paragraph is a list of 
    lines of the song. This makes further analysis more simple.
    '''
    result = []
    temp_para = []
    for line in lyrics.strip().split('\r\n'):
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
