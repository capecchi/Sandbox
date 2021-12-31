import os

if os.path.exists('C:/Users/Owner/Dropbox'):
	direc = 'C:/Users/Owner/Dropbox/grandmas_questions/'
elif os.path.exists('C:/Users/wcapecch/Dropbox'):
	direc = 'C:/Users/wcapecch/Dropbox/grandmas_questions/'
else:
	print('no good directory found-- where are you??')

files = [f for f in os.listdir(direc) if f.startswith('pagesource_')]

lines2write = []
num = 1
for file in files:
	print(f'analyzing {file}')
	lines2write.append('<b>' + file.replace('pagesource_', '').replace('.txt', '') + '</b><br><br>')
	with open(direc + file, 'r') as fread:
		lines = fread.readlines()
		for q in lines[0].split('"headline flex suggestion">')[1:]:
			newline = q.split('</div>')[0].replace('&#39;', '\'') + '<br>'
			if newline not in lines2write:
				lines2write.append(f'{num}. {newline}')
				num += 1
	lines2write.append('<br><br>')

with open(direc + 'grandmas_questions.html', 'w') as fwrite:
	fwrite.writelines(lines2write)
