import pandas as pd

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
text_data = {}
with open('script.txt', 'r') as bigl_script:
    
    line = bigl_script.readline()
    
    while line:
        
        # observe current content
        content = line.strip()
        leading_whitespace_count = len(line) - len(content)

        # read next content
        line = bigl_script.readline()
        
        # a new character starts talking
        if content in bigl_characters and leading_whitespace_count==character_start_whitespace_count:
            current_character = bigl_characters[content]
            if not current_character in text_data:
                text_data[current_character] = []
            text_data[current_character].append('')
            content_white_space_count = len(line)-len(line.strip())
        else:
            # a character is talking
            if current_character and abs(leading_whitespace_count-content_white_space_count)<3:
                text_data[current_character][-1] += f'{content} '
            # a character stops talking
            else:
                current_character = None

for character, samples in text_data.items():
    print(character)
    for sample in samples[:3]:
        print(f'\t{sample}')