class Graph:
    def __init__(self, vertices):
        self.v = vertices
        self.adj_list = {i : [] for i in range(vertices)}
        self.visited = [False] * vertices

    def addEdge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def DFS(self, node):
        self.visited[node] = True
        print(node, end=' ')

        for next in self.adj_list[node]:
            if not self.visited[next]:
                self.DFS(next)
    
    def reset(self):
        self.visited = [False] * self.v

g = Graph(5)
g.addEdge(0, 1)
g.addEdge(1, 2)
g.addEdge(1, 3)
g.addEdge(2, 4)

print("Depth First Traversal starting from node 0:")
g.DFS(0)