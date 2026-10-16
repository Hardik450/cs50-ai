#include <iostream>
#include <vector>

using namespace std;

class Graph{
    private:
        int v;
        vector<bool> visited;
        vector<vector<int>> adj;

    public:
    Graph(int vertices){
        v = vertices;
        visited.resize(v, false);
        adj.resize(v);
    }

    void addEdge(int u, int v){
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    void DFS(int node){
        visited[node] = true;
        cout << node << " ";

        for(int next : adj[node]){
            if(!visited[next]){
                DFS(next);
            }
        }
    }

    void resetVisited(){
        fill(visited.begin(), visited.end(), false);
    }
};

int main(){
    Graph G(5);
    G.addEdge(0, 1);
    G.addEdge(1, 2);
    G.addEdge(1, 3);
    G.addEdge(2, 4);
    cout << "DFS starting from node 0:" << endl;
    G.DFS(0);
}

// 📌 DFS Algorithm (Depth First Search)

// (using OOP concept — Graph object)

// Algorithm

// Start with a graph represented using a class (Graph object).

// Maintain a Visited list/array inside the Graph to mark visited nodes.

// Choose a starting node.

// Mark the starting node as visited.

// Process the node (e.g., display it).

// For every adjacent/unvisited neighboring node:

// Recursively apply DFS on that neighbor

// Continue until all reachable vertices are visited.

// Stop when no unvisited adjacent nodes remain and all recursive calls return.