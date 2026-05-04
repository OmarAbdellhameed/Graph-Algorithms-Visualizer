from collections import deque

# ───────────── DATA STRUCTURES ─────────────

class Queue:
    def __init__(self):
        self.data = deque()

    def enqueue(self, item):
        self.data.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.data.popleft()

    def is_empty(self):
        return len(self.data) == 0


class Stack:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.data.pop()

    def is_empty(self):
        return len(self.data) == 0


class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, priority, node):
        self.heap.append((priority, node))
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            raise IndexError("Heap is empty")

        self._swap(0, len(self.heap) - 1)
        item = self.heap.pop()
        if self.heap:
            self._heapify_down(0)
        return item

    def is_empty(self):
        return len(self.heap) == 0

    def _heapify_up(self, i):
        parent = (i - 1) // 2
        if i > 0 and self.heap[i][0] < self.heap[parent][0]:
            self._swap(i, parent)
            self._heapify_up(parent)

    def _heapify_down(self, i):
        smallest = i
        left = 2*i + 1
        right = 2*i + 2

        if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
            smallest = left
        if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
            smallest = right

        if smallest != i:
            self._swap(i, smallest)
            self._heapify_down(smallest)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]


# ───────────── GRAPH ─────────────

class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.adjacency = {}

    def add_node(self, node):
        if node not in self.adjacency:
            self.adjacency[node] = []

    def add_edge(self, u, v, w=1):
        self.add_node(u)
        self.add_node(v)
        self.adjacency[u].append((v, w))
        if not self.directed:
            self.adjacency[v].append((u, w))

    def get_nodes(self):
        return list(self.adjacency.keys())

    def get_neighbors(self, node):
        return self.adjacency.get(node, [])


# ───────────── BFS ─────────────

def bfs(graph, start):
    if start not in graph.adjacency:
        return {"error": "Start node not found"}

    visited = set([start])
    queue = Queue()
    queue.enqueue(start)
    steps = []

    while not queue.is_empty():
        node = queue.dequeue()
        steps.append({"action": "visit", "node": node})

        for neighbor, _ in graph.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)

    return {"steps": steps}


# ───────────── DFS ─────────────

def dfs(graph, start):
    if start not in graph.adjacency:
        return {"error": "Start node not found"}

    visited = set()
    stack = Stack()
    stack.push(start)
    steps = []

    while not stack.is_empty():
        node = stack.pop()
        if node in visited:
            continue

        visited.add(node)
        steps.append({"action": "visit", "node": node})

        for neighbor, _ in reversed(graph.get_neighbors(node)):
            if neighbor not in visited:
                stack.push(neighbor)

    return {"steps": steps}


# ───────────── DIJKSTRA ─────────────

def dijkstra(graph, start):
    INF = float("inf")
    dist = {node: INF for node in graph.get_nodes()}
    dist[start] = 0

    heap = MinHeap()
    heap.push(0, start)

    while not heap.is_empty():
        current_dist, node = heap.pop()

        for neighbor, w in graph.get_neighbors(node):
            new_dist = current_dist + w
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heap.push(new_dist, neighbor)

    return {"distances": dist}


# ───────────── BELLMAN-FORD ─────────────

def bellman_ford(graph, start):
    INF = float("inf")
    nodes = graph.get_nodes()
    dist = {node: INF for node in nodes}
    dist[start] = 0

    edges = []
    for u in graph.adjacency:
        for v, w in graph.adjacency[u]:
            edges.append((u, v, w))

    for _ in range(len(nodes) - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    return {"distances": dist}