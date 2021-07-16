class vertex:
    def __init__(self, node) -> None:
        self.id = node
        self.adjacent= {}

    def __str__(self) -> str:
        return(str(self.id)) + '--> adjacent nodes are : ' + str([x.id for x in self.adjacent])

    def add_neighbour(self,neighbour,weight = 0):
        self.adjacent[neighbour] = weight
    
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

    def add_edge(self,vertex_from,vertex_to,cost = 0):
        if vertex_from not in self.vertices:
            self.add_vertex(vertex_from)
        if vertex_to not in self.vertices:
            self.add_vertex(vertex_to) 
        
        self.vertices[vertex_from].add_neighbour(self.vertices[vertex_to],cost)
        self.vertices[vertex_to].add_neighbour(self.vertices[vertex_from],cost)


    def get_vertex(self,search):
        if search in self.vertices:
            return(self.vertices[search])
        else:
            return None

    def get_all_vertices(self):
        return(self.vertices.keys())


if __name__ =='__main__':
    g = Graph()

    g.add_vertex('a')
    g.add_vertex('b')
    g.add_vertex('c')
    g.add_vertex('d')
    g.add_vertex('e')
    g.add_vertex('f')

    g.add_edge('a','b',7)
    g.add_edge('a','c',9)
    g.add_edge('a','f',14)
    g.add_edge('b','c',10)
    g.add_edge('b','d',15)
    g.add_edge('c','d',11)
    g.add_edge('c','f',2)
    g.add_edge('d','e',6)
    g.add_edge('f','e',9)

    print(g.get_all_vertices())
    print(g.get_vertex('f'))
