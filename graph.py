

import os
import json


path_to_json ='./repos/iudx-voc/'
classes = ['owl:Class', 'rdfs:Class', 'rdf:Property']
properties = ["iudx:TextProperty", "iudx:QuantitativeProperty", "iudx:StructuredProperty", "iudx:GeoProperty", "iudx:TimeProperty", "iudx:Relationship"] 
relation = ["iudx:Relationship"]

error_list = []

                    

class Vertex:
    def __init__(self, node, vertice_type, jsonld, context) -> None:
        self.id = node
        self.node_type = vertice_type
        self.adjacent = {}
        self.jsonld = jsonld
        self.context = context

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
        
    def __iter__(self) -> None:
        return(iter(self.vertices.values()))

    def add_vertex(self, node, tp, jsonld, context):
        self.num_of_vertices = self.num_of_vertices + 1
        new_vertex = Vertex(node, tp, jsonld, context)
        self.vertices[node] = new_vertex
        return new_vertex

    def add_edge(self,vertex_from, vertex_to, relationship): 
        self.vertices[vertex_from].add_neighbour(self.vertices[vertex_to], relationship)
        
    def get_class_graph(self, v, out = [],cont = {}):
        for key, value in v.adjacent.items():
            if value == "domainOf":
                out.append(key.jsonld)
                cont["@context"] = key.context
            elif value == "subClassOf":
                out.append(key.jsonld)
                cont["@context"] = key.context
                self.get_class_graph(key, out)
            elif value == "rangeOf":
                out.append(key.jsonld)
                cont["@context"] = key.context
                self.get_class_graph(key, out)
            with open("context.json", "w") as context_file:
                json.dump(out, context_file)
                json.dump(cont, context_file)

    def get_vertex(self, search):
        if search in self.vertices:
            return(self.vertices[search])
        else:
            return None
    
    def get_all_vertices(self):
        return(self.vertices.keys())



class Vocabulary:
    
    def __init__(self, path_to_json):
        self.json_ld_graph = []
        self.context = {}
        self.read_repo(path_to_json)
        self.g = Graph()
        self.build_graph()

    def read_repo(self, path_to_json):
        for subdir, dirs, files in os.walk(path_to_json):
            for file in files:
                filepath = subdir + os.sep + file
                if filepath.endswith(".jsonld"):
                    with open(filepath,"r+") as input_file:
                        data = json.load(input_file)
                        if "@graph" in data:
                            self.json_ld_graph.append((data["@graph"][0])) 
                        if "@context" in data:
                            self.context["@context"] = data["@context"]
                        
                             
                                
                                    

    def build_graph(self):
        for n in self.json_ld_graph:
            try:
                # Making vertices of all classes  
                if (any(ele in classes for ele in n["@type"])):
                    tp = "Class"
                    self.g.add_vertex(n["@id"], tp, n, self.context["@context"])

                # Making vertices of all properties
                if (any(ele in properties for ele in n["@type"])):
                    tp = "Property"
                    self.g.add_vertex(n["@id"], tp, n, self.context["@context"])
            except:
                pass     

        for n in self.json_ld_graph:
                if "rdfs:subClassOf" in n:
                    try:
                        self.g.add_edge(n["@id"], n["rdfs:subClassOf"]["@id"], "subClassOf")
                    except Exception as error:
                        error_list.append({"type ": "subClassOf missing" , "in": n["@id"]})
                        pass
                        
                if "iudx:domainIncludes" in n :
                    for i in n["iudx:domainIncludes"]:
                        try:
                            self.g.add_edge(n["@id"], i["@id"], "domainIncludes")
                            self.g.add_edge(i["@id"], n["@id"], "domainOf")      
                        except Exception as error:
                            error_list.append({"type ": "domainIncludes missing" , "value": i["@id"], "in": n["@id"]})
                            pass
                        
                if "iudx:rangeIncludes" in n :
                    for i in n["iudx:rangeIncludes"]:
                        try:
                            self.g.add_edge(n["@id"], i["@id"], "rangeIncludes")
                            self.g.add_edge(i["@id"], n["@id"], "rangeOf")
                        except Exception as error:
                            error_list.append({"type" : "rangeIncludes missing", "value" : i["@id"], "in": n["@id"]})
                            pass

        with open("errors.json", "w") as out_file:
            json.dump(error_list, out_file)


def main():
    voc = Vocabulary("./repos/iudx-voc")
    n = voc.g.get_vertex("iudx:Resource")
    grph = []
    con = {}
    voc.g.get_class_graph(n, grph, con)



if __name__ == "__main__":
    main()
