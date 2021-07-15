import os
import glob

path = './repos/iudx-voc/'
contents = []
for root, directories, files in os.walk(path):
    for file in files:
        filepath = os.path.join(root, file)
        if filepath.endswith('.jsonld'):
            with open(file,'r') as filecontent:
                contents.append(file)
                print(contents)
            
