class Spot:
    """景点类"""
    def __init__(self, id, name, description, image_url, position, tags=None):
        self.id = id                  # 景点ID
        self.name = name              # 景点名称
        self.description = description # 景点描述
        self.image_url = image_url    # 景点图片URL
        self.position = position      # 景点位置坐标 (x, y)
        self.tags = tags or []        # 景点标签（如：历史遗迹、园林、宫殿等）
        
class ScenicArea:
    """景区类，使用图结构存储景点和路径"""
    def __init__(self, name):
        self.name = name              # 景区名称
        self.spots = {}               # 存储所有景点 {id: Spot对象}
        self.paths = {}               # 邻接表存储路径 {spot_id: [(neighbor_id, distance), ...]}
        
    def add_spot(self, spot):
        """添加景点"""
        self.spots[spot.id] = spot
        if spot.id not in self.paths:
            self.paths[spot.id] = []
            
    def add_path(self, spot1_id, spot2_id, distance):
        """添加两个景点之间的路径（无向图）"""
        if spot1_id not in self.spots or spot2_id not in self.spots:
            raise ValueError("景点不存在")
            
        # 添加双向路径
        self.paths[spot1_id].append((spot2_id, distance))
        self.paths[spot2_id].append((spot1_id, distance))
    
    def search_spots(self, keyword):
        """根据关键词搜索景点"""
        results = []
        for spot in self.spots.values():
            if (keyword.lower() in spot.name.lower() or 
                keyword.lower() in spot.description.lower() or
                any(keyword.lower() in tag.lower() for tag in spot.tags)):
                results.append(spot)
        return results
    
    def dijkstra(self, start_id):
        """使用Dijkstra算法计算从起点到所有其他点的最短路径"""
        import heapq
        
        # 初始化距离字典和前驱节点字典
        distances = {spot_id: float('infinity') for spot_id in self.spots}
        distances[start_id] = 0
        predecessors = {spot_id: None for spot_id in self.spots}
        
        # 优先队列
        priority_queue = [(0, start_id)]
        
        while priority_queue:
            current_distance, current_spot_id = heapq.heappop(priority_queue)
            
            # 如果已经找到更短的路径，跳过
            if current_distance > distances[current_spot_id]:
                continue
                
            # 检查所有邻居
            for neighbor_id, weight in self.paths[current_spot_id]:
                distance = current_distance + weight
                
                # 如果找到更短的路径，更新
                if distance < distances[neighbor_id]:
                    distances[neighbor_id] = distance
                    predecessors[neighbor_id] = current_spot_id
                    heapq.heappush(priority_queue, (distance, neighbor_id))
                    
        return distances, predecessors
    
    def shortest_path(self, start_id, end_id):
        """计算两点间的最短路径"""
        distances, predecessors = self.dijkstra(start_id)
        
        if distances[end_id] == float('infinity'):
            return None, float('infinity')  # 不可达
            
        # 重建路径
        path = []
        current = end_id
        while current:
            path.append(current)
            current = predecessors[current]
            
        path.reverse()  # 反转路径从起点到终点
        return path, distances[end_id]
    
    def minimum_spanning_tree(self):
        """使用Kruskal算法计算最小生成树"""
        # 边列表
        edges = []
        for u in self.paths:
            for v, weight in self.paths[u]:
                if u < v:  # 避免重复添加边
                    edges.append((u, v, weight))
        
        # 按权重排序
        edges.sort(key=lambda x: x[2])
        
        # 并查集
        parent = {spot_id: spot_id for spot_id in self.spots}
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            parent[find(x)] = find(y)
        
        # 最小生成树
        mst = []
        for u, v, weight in edges:
            if find(u) != find(v):
                union(u, v)
                mst.append((u, v, weight))
                
        return mst 