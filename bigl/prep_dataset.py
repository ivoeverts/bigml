import pandas as pd
import pickle
import re

# characters in the movie
bigl_characters = {c: c for c in (
    'DUDE', 'WALTER', 'DONNY', 'QUINTANA', 'BRANDT', 'MAUDE', 'LEBOWSKI', 
    'THE STRANGER', 'TREEHORN', 'CHIEF', 'DA FINO', 'DIETER'
)}

# 'BRANDT' is also denoted as 'YOUNG MAN'; so we should map observed names onto actual names
# same for the stranger's voice
bigl_characters.update({
    'YOUNG MAN': 'BRANDT',
    "THE STRANGER'S VOICE": 'THE STRANGER'
})

# when a new character starts, there are 33 trailing whitespaces before the name :-S
character_start_whitespace_count = 33
content_white_space_count = None

# collect paragraphs per character
current_character = None
samples = {}
with open('script.txt', 'r') as bigl_script:
    
    line = bigl_script.readline()
    
    while line:

        if line.startswith(' '):

            # observe current content
            content = line.replace('--', '').strip()
            is_start_of_character = content==content.upper()
            leading_whitespace_count = len(line) - len(content)
            
            # a new character starts talking
            if content in bigl_characters and leading_whitespace_count==character_start_whitespace_count:
                current_character = bigl_characters[content]
                if not current_character in samples:
                    samples[current_character] = []
                samples[current_character].append('')
            else:
                # a character is talking
                if current_character and not is_start_of_character: # and abs(leading_whitespace_count-content_white_space_count)<3:
                    samples[current_character][-1] += f'{content} '
                else:
                    current_character = None

        else:
            
            current_character = None

        # read next content
        line = bigl_script.readline()

# break into sentences and paragraphs
sentences, paragraphs = [], []

# break data down on paragraph and sentence level
for character in samples:
    print(f'{character}: {len(samples[character])}')
    
    for sample in samples[character]:
        
        if not len(sample):
            continue
        
        paragraphs.append({
            'character': character,
            'text': sample.strip()
        })
        sentences += [{'character': character, 'text': sentence}
                      for sentence in re.split('[!?.]', sample) if len(sentence.strip())]

# save to disk
for data_type, data in {'sentences': sentences, 'paragraphs': paragraphs}.items():
    pd.DataFrame(data).to_pickle(data_type)