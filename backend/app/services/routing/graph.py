from collections import defaultdict
import heapq

class RoadGraph:
    def __init__(self):
        # adjacency list: node -> list of (neighbor, base_time, segment_id)
        self.adj = defaultdict(list)
        # segment info: segment_id -> {'base_time': float, 'risk_score': float, 'confidence': float}
        self.segment_info = defaultdict(dict)

    def add_edge(self, from_node, to_node, segment_id, base_time):
        # Add both directions
        self.adj[from_node].append((to_node, base_time, segment_id))
        self.adj[to_node].append((from_node, base_time, segment_id))
        # Store base_time in segment_info too (for quick access)
        self.segment_info[segment_id]['base_time'] = base_time
        # Initialize risk_score and confidence with defaults
        self.segment_info[segment_id]['risk_score'] = 0.5
        self.segment_info[segment_id]['confidence'] = 0.5

    def set_risk(self, segment_id, risk_score, confidence):
        if segment_id in self.segment_info:
            self.segment_info[segment_id]['risk_score'] = risk_score
            self.segment_info[segment_id]['confidence'] = confidence

    def get_weight(self, segment_id, risk_penalty=1.0, uncertainty_penalty=300.0):
        info = self.segment_info.get(segment_id)
        if not info:
            # Should not happen if segment_id exists in graph, but return large weight
            return 999999.0
        base_time = info.get('base_time', 0.0)
        risk_score = info.get('risk_score', 0.5)
        confidence = info.get('confidence', 0.5)
        return base_time * (1 + risk_penalty * risk_score) + uncertainty_penalty * (1 - confidence)

    def shortest_path(self, start_node, end_node, risk_penalty=1.0, uncertainty_penalty=300.0):
        # Check if nodes exist
        if start_node not in self.adj or end_node not in self.adj:
            return None, None, float('inf')

        dist = {node: float('inf') for node in self.adj}
        prev = {node: None for node in self.adj}
        dist[start_node] = 0
        pq = [(0, start_node)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            if u == end_node:
                break
            for v, base_time, seg_id in self.adj[u]:
                weight = self.get_weight(seg_id, risk_penalty, uncertainty_penalty)
                new_dist = dist[u] + weight
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    prev[v] = u
                    heapq.heappush(pq, (new_dist, v))

        if dist[end_node] == float('inf'):
            return None, None, float('inf')

        # Reconstruct path
        path_nodes = []
        node = end_node
        while node is not None:
            path_nodes.append(node)
            node = prev[node]
        path_nodes.reverse()

        # Reconstruct segment list
        path_segments = []
        for i in range(len(path_nodes)-1):
            u, v = path_nodes[i], path_nodes[i+1]
            # Find segment id by checking adjacency
            for nb, bt, sid in self.adj[u]:
                if nb == v:
                    path_segments.append(sid)
                    break

        return path_nodes, path_segments, dist[end_node]