from collections import deque
class Graph:
    def __init__(self, vertices):
        self.ve = vertices
        self.visited = [False] * vertices
        self.adj = {v: [] for v in range(vertices)}

    def addEdges(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)

    def BFS(self, a):
        q = deque([a])
        self.visited[a] = True
        
        while q:
            b = q.popleft()
            print(b, end=" ")

            for next in self.adj[b]:
                if not self.visited[next]:
                   self.visited[next] = True
                   q.append(next)

g = Graph(5)
g.addEdges(0, 1)
g.addEdges(0, 2)
g.addEdges(1, 3)
g.addEdges(1, 4)
print('BFS:')
g.BFS(0)