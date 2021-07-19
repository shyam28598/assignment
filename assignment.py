# import os
# import glob

# path = './repos/iudx-voc/'
# contents = []
# for root, directories, files in os.walk(path):
#     for file in files:
#         filepath = os.path.join(root, file)
#         if filepath.endswith('.jsonld'):
#             contents.append((file))
                
import os,json

path_to_json = './repos/iudx-voc/'

class vertex:
    def __init__(self, node) -> None:
        self.id = node
        self.adjacent= {}

    def __str__(self) -> str:
        return(str(self.id)) + '--> adjacent nodes are : ' + str([x.id for x in self.adjacent])

    def add_neighbour(self,neighbour,relationship):
        self.adjacent[neighbour] = relationship
    
    def get_connections(self):
        return(self.adjacent.keys())

    def get_weight(self, neighbour):
        return(self.adjacent[neighbour])

    def get_id(self):
        return(self.id)

class Graph:
    def __init__(self) -> None:
        self.vertices = {}
        self.num_of_vertices = 0

    def __iter__(self) ->None:
        return(iter(self.vertices.values()))

    def add_vertex(self,node):
        self.num_of_vertices = self.num_of_vertices + 1
        new_vertex = vertex(node)
        self.vertices[node] =new_vertex
        return new_vertex

    def add_edge(self,vertex_from,vertex_to,relationship):
        if vertex_from not in self.vertices:
            self.add_vertex(vertex_from)
        if vertex_to not in self.vertices:
            self.add_vertex(vertex_to) 
        
        self.vertices[vertex_from].add_neighbour(self.vertices[vertex_to],relationship)
        self.vertices[vertex_to].add_neighbour(self.vertices[vertex_from],relationship)


    def get_vertex(self,search):
        if search in self.vertices:
            return(self.vertices[search])
        else:
            return None

    def get_all_vertices(self):
        return(self.vertices.keys())


graphs = []
id= []
g =Graph()
for root, directories, files in os.walk(path_to_json):
    for file in files:
        filepath = os.path.join(root, file)
        if filepath.endswith('.jsonld'):
            with open(filepath) as json_file:
                    data = json.load(json_file)
                    if '@graph'in data.keys():
                    #    print(data['@graph'])
                       for item in data['@graph']:
                            if "rdfs:Class" in item["@type"]:
                                print('Class Name ' + item["@id"])
                                g.add_vertex(item["@id"])
                            elif "iudx:TextProperty" or "iudx:QuantitativeProperty" or "iudx:StructuredProperty" or "iudx:GeoProperty" or "TimeProperty" in item["@type"]:
                                g.add_vertex(item["@id"])
                                print('Property Name '+ item["@id"])
                            elif "iudx:Relationship" in item["@type"]:
                                print('Relationship ' + item["@id"])
                # if '@graph' in data:
                #     graphs.append(data['@graph'])
                #     id.append(data['@graph'][0]['@id'])
                #     print(graphs)
                    # print(graphs[0][0]['@type'])
                # for item in grg.add_vertex(item["@id"])aphs:
                #     print(graphs)
                    # if "rdfs:Class" or "owl:Class" in item[0]['@type']:
                    #     print(item[0]['@id'])  
                    # print(item[0]['@type'])
                #     if "rdfs:Class" and "owl:Class" in item[0]['@type']:
                #         print(item[0]['@id'])
                    # elif 'Property' in typ:
                    #     print('Property Name : '+item[0]['@id'])
                    # elif 'Relationship'in item[0]['@type']:
                    #     print('Relationship :' +item[0]['@type'])
                
                
                
                # if '@graph' in graphs1:
                #     if 'iudx:TextProperty' or 'iudx:QuantitativeProperty' or 'iudx:StructuredProperty' or 'iudx:GeoProperty' in data['@graph'][0]['@type']:
                        # print(data['@graph'][0]['iudx:domainIncludes'])
                        # print(data['@graph'][0]['iudx:rangeIncludes'])
                        # print(graphs1)
                        # g.add_vertex(data['@graph'][0]['@id'])
                        # g.add_edge(data['@graph'][0]['@id'],data['@graph'][0]['iudx:domainIncludes'][0]['@id'],data['@graph'][0]['@type'][0])
                        # print(data['@graph'][0]['@type'][0])
                        # print(g.get_all_vertices())
                        # print(g.get_vertex('iudx:binID'))
                        # print(data['@graph'][0]['@id'])
                    # elif 'iudx:Relationship' in  data['@graph'][0]['@type'] :
                    #     g.add_edge(data['@graph'][0]['@id'],data['@graph'][0]['iudx:domainIncludes'],data['@graph'][0]['@type'])