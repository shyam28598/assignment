# Here is a template that you should follow
# Just put your code in between the respective comment sections
# Don't make the code ugly
# Don't delete the section "#" headings
# Retain all the #1, #2 comments. Those should have the relevant code right below them



# imports
import os
import json

# a. Big graph 
'''  Instructions
#1. Read all the jsonld documents in the directory
#2. Store all of the contents of @graph into a list `json_ld_graph`
#3. This should be done for all properties and classes irrespective of their type

Input: Path to voc repo
Output: List json_ld_graph
'''
path_to_json='./repos/iudx-voc/'
json_ld_graph=[]


for subdir, dirs, files in os.walk(path_to_json):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file

        if filepath.endswith(".jsonld"):
            # print (filepath)
            with open(filepath,"r+") as input_file:
                data=json.load(input_file)
                if "@graph" in data:
                    json_ld_graph.append((data["@graph"][0])) 
                    

                
                

# b. Class Vertex 
'''  Instructions
#1. Just copy paste the class here
Output: Class Vertex
'''
class Vertex:
    def __init__(self, node,vertice_type) -> None:
        self.id = node
        self.node_type = vertice_type
        self.adjacent= {}

    def __str__(self) -> str:
        return(str(self.id)) + ' domainIncludes : -->' + str([x.id for x in self.adjacent])

    def add_neighbour(self,neighbour,relationship):
        self.adjacent[neighbour] = relationship
    
    def get_connections(self):
        return(self.adjacent.keys())

    def get_weight(self, neighbour):
        return(self.adjacent[neighbour])

    def get_id(self):
        return(self.id)

    def get_type(self):
        return(self.node_type)

# c. Class Graph 
'''  Instructions
#1. Just copy paste the class here
Output: Class Graph
'''
class Graph:
    def __init__(self) -> None:
        self.vertices = {}
        self.num_of_vertices = 0

    def __iter__(self) ->None:
        return(iter(self.vertices.values()))

    def add_vertex(self,node,tp):
        self.num_of_vertices = self.num_of_vertices + 1
        new_vertex = Vertex(node,tp)
        self.vertices[node] =new_vertex
        return new_vertex

    def add_edge(self,vertex_from,vertex_to,relationship):
        if vertex_from not in self.vertices:
            self.add_vertex(vertex_from,tp)
        if vertex_to not in self.vertices:
            self.add_vertex(vertex_to,tp) 
        
        self.vertices[vertex_from].add_neighbour(self.vertices[vertex_to],relationship)
        self.vertices[vertex_to].add_neighbour(self.vertices[vertex_from],relationship)


    def get_vertex(self,search):
        if search in self.vertices:
            return(self.vertices[search])
        else:
            return None
    
    def get_all_vertices(self):
        return(self.vertices.keys())

# d. Initialize the graph 
'''  Instructions
#1. Initialize graph, Line 81 of your code
#2. Iterate through every element of of list json_ld_graph
     for n in json_ld_graph:
#3. For each element do this
    tp = <"class" if @type = rdfs or owl Class, "property" if @type = any of the properties>
    g.add_vertex(n["@id"], tp) # id, type
    if <any-property>:
        for each dIncl in domainIncludes
            g.add_edge(n["@id"], dIncl, "domainIncludes") # id, id of class, rel-name
        for each rIncl in rangeIncludes
            g.add_edge(n["@id"], rIncl, "rangeIncludes") # id, id of class, rel-name
    if <class>:
        g.add_edge(n["@id"], n["subClassOf"], "subClassOf") # id, id of class, rel-name
#5. Now graph g has all the vertices of all classes and properties along with the relationships
'''
g = Graph()
classes=['owl:Class','rdfs:Class']
properties= ["iudx:TextProperty","iudx:QuantitativeProperty" , "iudx:StructuredProperty" , "iudx:GeoProperty" , "iudx:TimeProperty","rdf:Property"] 
required=["iudx:domainIncludes"]
for n in json_ld_graph:
        # Making vertices of all classes  
        if (any(ele in classes for ele in n["@type"])):
            tp="Class"
            g.add_vertex(n["@id"],tp)

        if (any(ele in properties for ele in n["@type"])):
            tp = "Property"
            g.add_vertex(n["@id"],tp)
            if "iudx:domainIncludes" in n :
                for i in n["iudx:domainIncludes"]:
                    g.add_edge(i["@id"],n["@id"],"domainIncludes")
                    g.add_edge(n["@id"],i["@id"],"domainOf")
for v in g:
        for w in v.get_connections():
            vid = v.get_id()
            vtype=v.get_type()
            wtype=v.get_type()
            wid = w.get_id()
            # print ( vid,vtype,v.get_weight(w), wid)


for v in g:
    print ("g.vertices[%s,%s]=%s" %(v.get_id(),v.get_type(), g.vertices[v.get_id()]))
# print(g.get_all_vertices())
# print(g.get_vertex("iudx:LineString"))