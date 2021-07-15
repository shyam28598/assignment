import os,json

path_to_json = './repos/iudx-voc/'

graphs = []
id= []
for root, directories, files in os.walk(path_to_json):
    for file in files:
        filepath = os.path.join(root, file)
        if filepath.endswith('.jsonld'):
            with open(filepath) as json_file:
                data = json.load(json_file)
                if '@graph' in data:
                    graphs.append(data['@graph'])
                    id.append(data['@graph'][0]['@id'])
                    print(id)