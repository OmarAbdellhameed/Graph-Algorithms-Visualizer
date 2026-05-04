# 📊 Graph Algorithm Visualizer

An interactive web-based tool for visualizing fundamental graph algorithms such as BFS and others. Built with **Flask (Python)** on the backend and a dynamic **HTML/CSS/JS frontend**, this project helps users understand how graph traversal algorithms work step by step.

---

## 🚀 Features

- 🔍 Visualize graph traversal algorithms
- 🔄 Supports **directed** and **undirected** graphs
- ⚖️ Weighted edges support
- 🧠 Step-by-step execution with detailed states
- 🌐 Interactive UI for building custom graphs

---

## 🧱 Project Structure

```
Graph Visualizer/
│
├── app.py                 # Flask backend (API + routing)
├── algorithms.py          # Data structures & algorithm logic
│
└── templates/
    └── index.html        # Frontend interface
```

---

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/OmarAbdellhameed/Graph-Algorithms-Visualizer.git
cd graph-visualizer
```

2. Install dependencies:
```bash
pip install flask
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and go to:
```
http://127.0.0.1:5000/
```

---

## 🧪 Supported Algorithms

- **Breadth-First Search (BFS)**
- **Depth-First Search (DFS)**
- **Dijkstra**
- **Bellman-Ford**

---

## 📡 API Endpoint

### `POST /api/run`

Runs a selected graph algorithm.

#### Request Body:
```json
{
  "algorithm": "bfs",
  "nodes": ["A", "B", "C"],
  "edges": [
    {"from": "A", "to": "B", "weight": 1},
    {"from": "B", "to": "C", "weight": 2}
  ],
  "start": "A",
  "directed": false
}
```

#### Response:
Returns a list of steps showing how the algorithm progresses.

---

## 🧠 Core Concepts Implemented

- Queue (for BFS)
- Stack (for DFS – extendable)
- Min Heap (for priority-based algorithms like Dijkstra)
- Graph representation using adjacency lists

---

## 🎨 Frontend

- Built with pure HTML, CSS, and JavaScript
- Dark-themed UI for better visualization
- Real-time animation of algorithm steps

---

## 📌 Future Improvements

- Save/load graph configurations
- Performance metrics visualization
- Sumultanous Comparisons between algorithms
