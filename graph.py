

import os
import json


path_to_json ='./repos/iudx-voc/'
json_ld_graph = []
classes = ['owl:Class', 'rdfs:Class']
properties = ["iudx:TextProperty", "iudx:QuantitativeProperty", "iudx:StructuredProperty", "iudx:GeoProperty", "iudx:TimeProperty", "rdf:Property"] 
relation = ["iudx:Relationship"]
blank = []
for subdir, dirs, files in os.walk(path_to_json):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file

        if filepath.endswith(".jsonld"):
            # print (filepath)
            with open(filepath,"r+") as input_file:
                data = json.load(input_file)
                if "@graph" in data:
                    json_ld_graph.append((data["@graph"][0])) 
                    

                
                


class Vertex:
    def __init__(self, node, vertice_type, jsonld) -> None:
        self.id = node
        self.node_type = vertice_type
        self.adjacent = {}
        self.jsonlist = list(jsonld)

    def __str__(self) -> str:
        print(str(self.id))

    def add_neighbour(self, neighbour, relationship):
        self.adjacent[neighbour] = relationship
    
    def get_connections(self):
        return(self.adjacent.keys())

    def get_weight(self, neighbour):
        return(self.adjacent[neighbour])

    def get_id(self):
        return(self.id)

    def get_type(self):
        return(self.node_type)


            

class Graph:
    def __init__(self) -> None:
        self.vertices = {}
        self.num_of_vertices = 0
        
    def __iter__(self) ->None:
        return(iter(self.vertices.values()))

    def add_vertex(self, node, tp, jsonld):
        self.num_of_vertices = self.num_of_vertices + 1
        new_vertex = Vertex(node, tp, jsonld)
        self.vertices[node] = new_vertex
        return new_vertex

    def add_edge(self,vertex_from, vertex_to, relationship): 
        self.vertices[vertex_from].add_neighbour(self.vertices[vertex_to], relationship)
        
    def get_class_graph(self, v, out = []):
        for key, value in v.adjacent.items():
            if value == "domainOf":
                out.append(key.id)
            elif value == "subClassOf":
                out.append(key.id)
                self.get_class_graph(key)

    def get_vertex(self, search):
        if search in self.vertices:
            return(self.vertices[search])
        else:
            return None
    
    def get_all_vertices(self):
        return(self.vertices.keys())



g = Graph()

for n in json_ld_graph:
    try:
        # Making vertices of all classes  
        if (any(ele in classes for ele in n["@type"])):
            tp = "Class"
            g.add_vertex(n["@id"], tp, n)
        # Making vertices of all properties
        if (any(ele in properties for ele in n["@type"])):
            tp = "Property"
            g.add_vertex(n["@id"], tp, n)
    except:
        pass     

for n in json_ld_graph:
        if "rdfs:subClassOf" in n:
            try:
                g.add_edge(n["@id"], n["rdfs:subClassOf"]["@id"], "subClassOf")
            except:
                pass 
             
        if "iudx:domainIncludes" in n :
            for i in n["iudx:domainIncludes"]:
                try:
                    g.add_edge(n["@id"], i["@id"], "domainIncludes")
                    g.add_edge(i["@id"], n["@id"], "domainOf")      
                except:
                    pass
                


n = g.get_vertex("iudx:Resource")
g.get_class_graph(n,blank)
print(blank)