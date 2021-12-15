"""
This routine takes an .MBOX file and separates out the puzzles, hints, pushes, and solutions
To obtain an .MBOX file for the MoMath mindbenders, go to https://takeout.google.com/
deselect all, then scroll down and select gmail
click on the "All Mail data included" button
deselect all, then select only the Interesting/MoMathMindBenders
click OK, then Next step at the bottom
export once, .zip file type, and 2GB is fine (first time I did this it was only ~1MB
create export, then download and extract once it's ready
"""

import numpy as np

direc = 'C:/Users/Owner/Dropbox/jens_gift/'
mbox = direc + 'Interesting-MoMathMindBenders.mbox'
with open(mbox, 'r') as file:
    lines = file.readlines()

puzzles = {}
for i in np.arange(len(lines)):
    if 'PUZZLE + PUSH' in lines[i]:  # next section contains puzzle, hint, and push
        newpush, newhint, newpuzzle = [], [], []
        while not lines[i].startswith('PUSH:'):
            i += 1
        while not lines[i].startswith('As a refresher'):
            newpush.append(lines[i].replace('PUSH: ', '').replace('\n', ' '))
            i += 1
        while not lines[i].startswith('PUZZLE:'):
            i += 1
        puzzname = ' '.join(lines[i].split(' ')[1:-1]).replace('&#39;', '\'')
        i += 2  # skip over blank line
        while not lines[i].startswith('HINT:'):
            newpuzzle.append(lines[i].replace('\n', ' '))
            i += 1
        while not lines[i].startswith('On Saturday'):
            newhint.append(lines[i].replace('HINT: ', '').replace('\n', ' '))
            i += 1
        if puzzname.startswith('THE KING'):# == 'PI SQUARED OVER SIX':
            a=1
        newpuzzle = ''.join([ll if ll != ' ' else '\n' for ll in newpuzzle]) + '\n\n'
        newhint = ''.join([ll if ll != ' ' else '\n' for ll in newhint]) + '\n\n'
        newpush = ''.join([ll if ll != ' ' else '\n' for ll in newpush]) + '\n\n'
        if puzzname in puzzles.keys():
            puzzles[puzzname].update({'puzzle': newpuzzle, 'hint': newhint, 'push': newpush})
        else:
            puzzles[puzzname] = {'puzzle': newpuzzle, 'hint': newhint, 'push': newpush}
    if 'PUZZLE SOLUTION' in lines[i]:  # next section contains solution. duh
        newsolution = []
        while not lines[i].startswith('PUZZLE:'):
            i += 1
        puzzname = ' '.join(lines[i].split(' ')[1:-1])
        while not lines[i].startswith('SOLUTION:'):
            i += 1
        while not lines[i].startswith('If you wish,') and not lines[i].startswith('If you enjoyed'):
            newsolution.append(lines[i].replace('SOLUTION: ', '').replace('\n', ' '))
            i += 1
        newsolution = ''.join([ll if ll != ' ' else '\n' for ll in newsolution]) + '\n\n'
        if puzzname in puzzles.keys():
            puzzles[puzzname].update({'solution': newsolution})
        else:
            puzzles[puzzname] = {'solution': newsolution}

# check dict
print(f'checking {len(puzzles.keys())} puzzles in dict')
badkeys = []
for k in puzzles.keys():
    if 'puzzle' not in puzzles[k].keys():
        print(f'missing the puzzle for {k}')
        badkeys.append(k)
    if 'hint' not in puzzles[k].keys():
        print(f'missing the hint for {k}')
        badkeys.append(k)
    if 'push' not in puzzles[k].keys():
        print(f'missing the push for {k}')
        badkeys.append(k)
    if 'solution' not in puzzles[k].keys():
        print(f'missing the solution for {k}')
        badkeys.append(k)
for k in np.unique(badkeys):
    puzzles.pop(k)
print(f'found {len(puzzles.keys())} good puzzles')

puzztxt, hinttxt, pushtxt, solutiontxt = [], [], [], []
for k in sorted(puzzles.keys()):  # sort alphabetically
    puzztxt.append(k + '\n\n')
    for line in puzzles[k]['puzzle']:
        puzztxt.append(line)
    hinttxt.append(k + '\n\n')
    for line in puzzles[k]['hint']:
        hinttxt.append(line)
    pushtxt.append(k + '\n\n')
    for line in puzzles[k]['push']:
        pushtxt.append(line)
    solutiontxt.append(k + '\n\n')
    for line in puzzles[k]['solution']:
        solutiontxt.append(line)

# write documents
with open(direc + 'puzzles.txt', 'w') as file:
    file.writelines(puzztxt)
print('wrote puzzle doc')
with open(direc + 'hints.txt', 'w') as file:
    file.writelines(hinttxt)
print('wrote hints doc')
with open(direc + 'pushes.txt', 'w') as file:
    file.writelines(pushtxt)
print('wrote pushes doc')
with open(direc + 'solutions.txt', 'w') as file:
    file.writelines(solutiontxt)
print('wrote solutions doc')
