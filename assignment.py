# import os,json

# path_to_json = ['/home/shyam/repos/iudx-voc/base-schemas/classes/','/home/shyam/repos/iudx-voc/base-schemas/properties/']

# for file_name in [file for file in os.listdir(path_to_json) if file.endswith('.jsonld')]:
#   with open(path_to_json + file_name) as json_file:
#     data = json.load(json_file)
#     print(file_name)

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
            
