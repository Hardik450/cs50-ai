#include <iostream>
#include <vector>
#include <queue>

using namespace std;

class Graph{
    private:
    int ve;
    vector<bool> visited;
    vector<vector<int>> adj;

    public:
    Graph(int vertices){
        ve = vertices;
        visited.resize(ve, false);
        adj.resize(ve);
    }

    void addEdges(int u, int v){
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    void BFS(int node){
        queue<int> q;
        visited[node] = true;
        q.push(node);

        while(!q.empty()){
            int a = q.front();
            q.pop();
            cout << a << " ";

            for(int next : adj[a]){
                if(!visited[next]){
                    visited[next] = true;
                    q.push(next);
                }
            }
        }
    }

};
int main(){
    Graph G(5);
    G.addEdges(0, 1);
    G.addEdges(0, 2);
    G.addEdges(1, 3);
    G.addEdges(1, 4);

    cout << "BFS: \n";
    G.BFS(0);
}