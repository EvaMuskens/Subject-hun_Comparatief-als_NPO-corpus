"""
Last version: Jan 12 2026
Author: EvaMuskens
"""

import spacy, re, os, time

# Alleen de eerste keer:
#spacy.cli.download("nl_core_news_lg")

start = time.perf_counter()

nlp = spacy.load("nl_core_news_lg")

subjects = {}
subjects['ze'] = 0
subjects['zij'] = 0
subjects['hun'] = 0

comparatives = {}
comparatives['dan'] = 0
comparatives['als'] = 0

n = 1

for filename in os.listdir('tekst_output_Amberscript'):
    
    print(n, filename, '\n')
    n += 1
    
    path = os.path.join('tekst_output_Amberscript', filename)
    file = open(path, 'r')
    raw_text = file.read()
    file.close()
    
    blocks = raw_text.split("\n\n")
    
    # Subject-hun:
    
    for block in blocks:
        
        lines = block.split("\n")
        timestamp = lines[0]
        text = lines[1]
        doc = nlp(text)
        
        for sent in doc.sents:
            for token in sent:
                if re.search(r'VNW\|pers\|pron\|.*\|3p?\|mv', token.tag_) and token.dep_ == 'nsubj':
                    if token.text.lower() =='ze':
                        subjects['ze'] += 1
                        #print(filename, timestamp, token,'\n')
                    if token.text.lower() == 'zij':
                        subjects['zij'] += 1
                        #print(filename, timestamp, token,'\n')
                    if token.text.lower() == 'hun':
                        subjects['hun'] += 1
                        #print(filename, timestamp, token,'\n')

    # comparatief+als:
    
    for block in blocks:
        
        lines = block.split("\n")
        timestamp = lines[0]
        text = lines[1]
        doc = nlp(text)
        
        for sent in doc.sents:
            tokens = list(sent)
            for i in range(len(tokens)):
                current_token = tokens[i]
                next_tokens = tokens[i+1:]
                if re.search (r'\|comp', current_token.tag_):
                    for token in next_tokens:
                        if token.dep_ == 'mark':
                            if token.text == 'als':
                                comparatives['als'] += 1
                                #print(filename, timestamp, current_token, next_tokens, '\n')
                            if token.text == 'dan':
                                comparatives['dan'] += 1
                                #print(filename, timestamp, current_token, next_tokens, '\n')

print('total subjects:', subjects, '\n')
print('total comparatives:', comparatives, '\n')

end = time.perf_counter()
print(f'runtime: {end - start:.2f} seconds')

