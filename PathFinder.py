import heapq
class PathFinder:
    def __init__(self):
        pass

    def find_path(self,adj_list, start, end):
        if start not in adj_list or end not in adj_list:
            return []

        # 初始化数据结构
        distances = {node: float('inf') for node in adj_list}
        distances[start] = 0
        predecessors = {node: None for node in adj_list}
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_node == end:
                break

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in adj_list.get(current_node, []):
                new_distance = current_distance + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor))

        path = []
        current = end
        while current is not None:
            path.append((current, distances[current]))
            current = predecessors[current]
        path.reverse()
        #返回包含节点和累计距离的路径列表，格式：[(节点ID, 累计距离), ...]
        return path if path and path[0][0] == start else []

    def calculate_distance(self,weighted_path):
        return weighted_path[-1][1] if weighted_path else 0
