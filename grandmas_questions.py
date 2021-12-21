import os

import numpy as np

direc = 'C:/Users/Owner/Dropbox/grandmas_questions/'
files = [f for f in os.listdir(direc) if f.startswith('pagesource_')]

lines2write = []
for file in files:
    print(f'analyzing {file}')
    lines2write.append('<b>'+file.replace('pagesource_', '').replace('.txt', '') + '</b><br><br>')
    with open(direc + file, 'r') as fread:
        lines = fread.readlines()
        for q in lines[0].split('"headline flex suggestion">')[1:]:
            newline = q.split('</div>')[0].replace('&#39;', '\'')+'<br>'
            if newline not in lines2write:
                lines2write.append(newline)
    lines2write.append('<br><br>')

with open(direc + 'grandmas_questions.html', 'w') as fwrite:
    fwrite.writelines(lines2write)
