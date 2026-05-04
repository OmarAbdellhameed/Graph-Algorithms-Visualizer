from flask import Flask, render_template, request, jsonify
from collections import deque
import heapq

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/run", methods=["POST"])
def run_algorithm():
    data = request.json
    algo = data["algorithm"]
    nodes = data["nodes"]
    edges = data["edges"]
    start = data["start"]
    directed = data["directed"]

    # Build adjacency list
    graph = {n: [] for n in nodes}
    for e in edges:
        w = float(e["weight"])
        graph[e["from"]].append((e["to"], w))
        if not directed:
            graph[e["to"]].append((e["from"], w))

    steps = []

    # --- BFS ---
    if algo == "bfs":
        visited = []
        queue = deque([start])
        seen = {start}
        while queue:
            curr = queue.popleft()
            visited.append(curr)
            steps.append({
                "action": "visit", "node": curr, "visited": list(visited),
                "description": f"Visiting node {curr}"
            })
            for neighbor, _ in graph[curr]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
                    steps.append({
                        "action": "relax", "node": neighbor, "from": curr, "visited": list(visited),
                        "description": f"Discovered {neighbor} from {curr}"
                    })

    # --- DFS ---
    elif algo == "dfs":
        visited = []
        stack = [start]
        seen = set()
        while stack:
            curr = stack.pop()
            if curr in seen: continue
            seen.add(curr)
            visited.append(curr)
            steps.append({
                "action": "visit", "node": curr, "visited": list(visited),
                "description": f"Visiting node {curr}"
            })
            # Reverse for consistent visualization of stack order
            for neighbor, _ in reversed(graph[curr]):
                if neighbor not in seen:
                    stack.append(neighbor)

    # --- DIJKSTRA ---
    elif algo == "dijkstra":
        dist = {n: "∞" for n in nodes}
        dist[start] = 0
        paths = {n: [start] for n in nodes}
        pq = [(0, start)]
        visited = []

        steps.append({"action": "start", "node": start, "distances": dict(dist), "description": f"Start Dijkstra at {start}"})

        while pq:
            d, curr = heapq.heappushpop(pq) if False else heapq.heappop(pq)
            if curr in visited: continue
            visited.append(curr)
            
            steps.append({
                "action": "visit", "node": curr, "visited": list(visited), 
                "distances": dict(dist), "paths": dict(paths),
                "description": f"Processing node {curr} (min dist: {d})"
            })

            for neighbor, weight in graph[curr]:
                old_d = float('inf') if dist[neighbor] == "∞" else dist[neighbor]
                if d + weight < old_d:
                    dist[neighbor] = d + weight
                    paths[neighbor] = paths[curr] + [neighbor]
                    heapq.heappush(pq, (dist[neighbor], neighbor))
                    steps.append({
                        "action": "relax", "node": neighbor, "from": curr, "distances": dict(dist),
                        "description": f"Relaxed {neighbor}: new distance {dist[neighbor]}"
                    })

    # --- BELLMAN-FORD ---
    elif algo == "bellman_ford":
        dist = {n: "∞" for n in nodes}
        dist[start] = 0
        paths = {n: [start] for n in nodes}
        
        for i in range(len(nodes) - 1):
            changed = False
            for u in nodes:
                for v, w in graph[u]:
                    u_d = float('inf') if dist[u] == "∞" else dist[u]
                    v_d = float('inf') if dist[v] == "∞" else dist[v]
                    if u_d + w < v_d:
                        dist[v] = u_d + w
                        paths[v] = paths[u] + [v]
                        changed = True
                        steps.append({
                            "action": "relax", "node": v, "from": u, "distances": dict(dist),
                            "description": f"Iteration {i+1}: {u} -> {v} updated to {dist[v]}"
                        })
            if not changed: break

    steps.append({"action": "done", "description": "Algorithm execution finished.", "visited": steps[-1].get("visited", []) if steps else []})
    return jsonify({"steps": steps, "distances": steps[-2].get("distances", {}) if algo in ["dijkstra", "bellman_ford"] else None})

if __name__ == "__main__":
    app.run(debug=True, port=5000)