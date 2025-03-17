<template>
          <div class="scenic-area-detail">
                    <div v-if="loading" class="loading-overlay">
                              <div class="loading-spinner"></div>
                              <span>正在加载...</span>
                    </div>

                    <div v-else class="scenic-detail-content">
                              <div class="detail-header">
                                        <h2>{{ name }}</h2>
                                        <div class="location-info">
                                                  <i class="fas fa-map-marker-alt"></i>
                                                  <span>经度: {{ lng.toFixed(4) }}, 纬度: {{ lat.toFixed(4) }}</span>
                                        </div>
                              </div>

                              <!-- 功能选择区 -->
                              <div class="function-tabs">
                                        <button 
                                                  v-for="tab in tabs" 
                                                  :key="tab.id"
                                                  :class="['tab-btn', { active: currentTab === tab.id }]"
                                                  @click="currentTab = tab.id"
                                        >
                                                  <i :class="tab.icon"></i>
                                                  {{ tab.name }}
                                        </button>
                              </div>

                              <!-- 搜索框 -->
                              <div class="search-box" v-if="currentTab !== 'path'">
                                        <input 
                                                  type="text" 
                                                  v-model="searchQuery" 
                                                  placeholder="搜索景点..." 
                                                  @input="handleSearch"
                                        >
                              </div>

                              <!-- 景点分布图 -->
                              <div v-if="currentTab === 'map'" class="map-view">
                                        <svg :width="mapWidth" :height="mapHeight" class="map-svg">
                                                  <!-- 连接线 -->
                                                  <g class="connections">
                                                            <line 
                                                                      v-for="(connection, index) in visibleConnections" 
                                                                      :key="'conn-' + index"
                                                                      :x1="connection.from.x" 
                                                                      :y1="connection.from.y"
                                                                      :x2="connection.to.x" 
                                                                      :y2="connection.to.y"
                                                                      :class="['connection-line', { 'path-line': isInPath(connection) }]"
                                                            />
                                                  </g>
                                                  
                                                  <!-- 景点节点 -->
                                                  <g 
                                                            v-for="spot in visibleSpots" 
                                                            :key="spot.id" 
                                                            class="spot-node"
                                                            @click="handleSpotClick(spot)"
                                                  >
                                                            <circle 
                                                                      :cx="spot.x" 
                                                                      :cy="spot.y" 
                                                                      :r="8"
                                                                      :class="['spot-circle', { 'selected': selectedSpot === spot }]"
                                                            />
                                                            <text 
                                                                      :x="spot.x" 
                                                                      :y="spot.y - 15" 
                                                                      text-anchor="middle"
                                                            >{{ spot.name }}</text>
                                                  </g>
                                        </svg>
                              </div>

                              <!-- 路径规划 -->
                              <div v-if="currentTab === 'path'" class="path-planning">
                                        <div class="path-inputs">
                                                  <select v-model="startSpot" class="spot-select">
                                                            <option value="">选择起点</option>
                                                            <option v-for="spot in spots" :key="'start-'+spot.id" :value="spot">
                                                                      {{ spot.name }}
                                                            </option>
                                                  </select>
                                                  <select v-model="endSpot" class="spot-select">
                                                            <option value="">选择终点</option>
                                                            <option v-for="spot in spots" :key="'end-'+spot.id" :value="spot">
                                                                      {{ spot.name }}
                                                            </option>
                                                  </select>
                                                  <button 
                                                            @click="findShortestPath" 
                                                            :disabled="!startSpot || !endSpot"
                                                            class="find-path-btn"
                                                  >
                                                            查找最短路径
                                                  </button>
                                        </div>

                                        <!-- 路径结果显示 -->
                                        <div v-if="shortestPath.length > 0" class="path-result">
                                                  <h3>最短路径：</h3>
                                                  <div class="path-steps">
                                                            <div 
                                                                      v-for="(spot, index) in shortestPath" 
                                                                      :key="'path-'+spot.id" 
                                                                      class="path-step"
                                                            >
                                                                      <div class="step-number">{{ index + 1 }}</div>
                                                                      <div class="step-content">
                                                                                <span class="spot-name">{{ spot.name }}</span>
                                                                                <span v-if="index < shortestPath.length - 1" class="distance">
                                                                                          ↓ {{ getDistance(spot, shortestPath[index + 1]) }}米
                                                                                </span>
                                                                      </div>
                                                            </div>
                                                  </div>
                                        </div>
                              </div>

                              <!-- 景点列表 -->
                              <div v-if="currentTab === 'list'" class="spot-list">
                                        <div 
                                                  v-for="spot in visibleSpots" 
                                                  :key="'list-'+spot.id" 
                                                  class="spot-item"
                                                  @click="handleSpotClick(spot)"
                                        >
                                                  <h3>{{ spot.name }}</h3>
                                                  <p>{{ spot.description }}</p>
                                        </div>
                              </div>
                    </div>
          </div>
</template>

<script>
export default {
          name: 'ScenicAreaDetail',
          props: {
                    name: {
                              type: String,
                              required: true
                    },
                    lat: {
                              type: Number,
                              required: true
                    },
                    lng: {
                              type: Number,
                              required: true
                    }
          },
          data() {
                    return {
                              loading: true,
                              currentTab: 'map',
                              searchQuery: '',
                              mapWidth: 800,
                              mapHeight: 600,
                              selectedSpot: null,
                              startSpot: null,
                              endSpot: null,
                              shortestPath: [],
                              tabs: [
                                        { id: 'map', name: '景区地图', icon: 'fas fa-map' },
                                        { id: 'list', name: '景点列表', icon: 'fas fa-list' },
                                        { id: 'path', name: '路径规划', icon: 'fas fa-route' }
                              ],
                              // 示例数据
                              spots: [
                                        { id: 1, name: '入口', x: 100, y: 300, description: '景区主入口' },
                                        { id: 2, name: '游客中心', x: 200, y: 200, description: '提供导游服务' },
                                        { id: 3, name: '观景台', x: 400, y: 150, description: '最佳观景位置' },
                                        { id: 4, name: '休息区', x: 300, y: 400, description: '供游客休息' },
                                        { id: 5, name: '纪念品商店', x: 500, y: 300, description: '销售特色商品' }
                              ],
                              // 景点之间的连接关系（邻接表）
                              connections: [
                                        { from: 1, to: 2, distance: 150 },
                                        { from: 2, to: 3, distance: 200 },
                                        { from: 2, to: 4, distance: 180 },
                                        { from: 3, to: 5, distance: 250 },
                                        { from: 4, to: 5, distance: 160 }
                              ]
                    };
          },
          computed: {
                    visibleSpots() {
                              if (!this.searchQuery) return this.spots;
                              const query = this.searchQuery.toLowerCase();
                              return this.spots.filter(spot => 
                                        spot.name.toLowerCase().includes(query) ||
                                        spot.description.toLowerCase().includes(query)
                              );
                    },
                    visibleConnections() {
                              return this.connections.map(conn => ({
                                        from: this.getSpotById(conn.from),
                                        to: this.getSpotById(conn.to),
                                        distance: conn.distance
                              }));
                    }
          },
          methods: {
                    getSpotById(id) {
                              return this.spots.find(s => s.id === id);
                    },
                    handleSpotClick(spot) {
                              this.selectedSpot = spot;
                    },
                    handleSearch() {
                              // 搜索功能已通过计算属性实现
                    },
                    getDistance(spot1, spot2) {
                              const connection = this.connections.find(c => 
                                        (c.from === spot1.id && c.to === spot2.id) ||
                                        (c.from === spot2.id && c.to === spot1.id)
                              );
                              return connection ? connection.distance : 0;
                    },
                    isInPath(connection) {
                              if (this.shortestPath.length < 2) return false;
                              for (let i = 0; i < this.shortestPath.length - 1; i++) {
                                        const curr = this.shortestPath[i];
                                        const next = this.shortestPath[i + 1];
                                        if ((connection.from.id === curr.id && connection.to.id === next.id) ||
                                                  (connection.from.id === next.id && connection.to.id === curr.id)) {
                                                  return true;
                                        }
                              }
                              return false;
                    },
                    findShortestPath() {
                              if (!this.startSpot || !this.endSpot) return;
                              
                              // Dijkstra算法实现最短路径
                              const distances = new Map();
                              const previous = new Map();
                              const unvisited = new Set(this.spots);
                              
                              // 初始化距离
                              this.spots.forEach(spot => {
                                        distances.set(spot, spot === this.startSpot ? 0 : Infinity);
                              });
                              
                              while (unvisited.size > 0) {
                                        // 找到距离最小的未访问节点
                                        let current = Array.from(unvisited).reduce((min, spot) => 
                                                  distances.get(spot) < distances.get(min) ? spot : min
                                        );
                                        
                                        if (current === this.endSpot) break;
                                        
                                        unvisited.delete(current);
                                        
                                        // 更新相邻节点的距离
                                        this.connections
                                                  .filter(conn => conn.from === current.id || conn.to === current.id)
                                                  .forEach(conn => {
                                                            const neighbor = this.getSpotById(
                                                                      conn.from === current.id ? conn.to : conn.from
                                                            );
                                                            if (!unvisited.has(neighbor)) return;
                                                            
                                                            const alt = distances.get(current) + conn.distance;
                                                            if (alt < distances.get(neighbor)) {
                                                                      distances.set(neighbor, alt);
                                                                      previous.set(neighbor, current);
                                                            }
                                                  });
                              }
                              
                              // 构建路径
                              const path = [];
                              let current = this.endSpot;
                              while (current) {
                                        path.unshift(current);
                                        current = previous.get(current);
                              }
                              
                              this.shortestPath = path;
                    }
          },
          async mounted() {
                    try {
                              // 模拟加载延迟
                              await new Promise(resolve => setTimeout(resolve, 500));
                    } finally {
                              this.loading = false;
                    }
          }
};
</script>

<style scoped>
.scenic-area-detail {
          padding: 20px;
          max-width: 1200px;
          margin: 0 auto;
          min-height: 400px;
          position: relative;
}

.loading-overlay {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(255, 255, 255, 0.8);
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          z-index: 1000;
}

.loading-spinner {
          width: 40px;
          height: 40px;
          border: 4px solid #f3f3f3;
          border-top: 4px solid #42b983;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin-bottom: 10px;
}

@keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
}

.detail-header {
          margin-bottom: 20px;
          padding-bottom: 15px;
          border-bottom: 1px solid #eee;
}

.detail-header h2 {
          margin: 0 0 10px 0;
          color: #333;
}

.location-info {
          color: #666;
          font-size: 0.9rem;
          display: flex;
          align-items: center;
          gap: 8px;
}

.detail-body {
          display: grid;
          grid-template-columns: 2fr 1fr;
          gap: 20px;
}

.map-container {
          background: #f5f5f5;
          border-radius: 8px;
          min-height: 400px;
}

.map-placeholder {
          height: 100%;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          color: #666;
}

.map-placeholder i {
          font-size: 3rem;
          margin-bottom: 10px;
}

.info-container {
          background: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
          .detail-body {
                    grid-template-columns: 1fr;
          }
}

.function-tabs {
          display: flex;
          gap: 10px;
          margin-bottom: 20px;
}

.tab-btn {
          padding: 8px 16px;
          border: none;
          border-radius: 4px;
          background: #f5f5f5;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 8px;
}

.tab-btn.active {
          background: #42b983;
          color: white;
}

.search-box {
          margin-bottom: 20px;
}

.search-box input {
          width: 100%;
          padding: 8px;
          border: 1px solid #ddd;
          border-radius: 4px;
}

.map-svg {
          border: 1px solid #ddd;
          border-radius: 4px;
          background: #fff;
}

.connection-line {
          stroke: #ddd;
          stroke-width: 2;
}

.path-line {
          stroke: #42b983;
          stroke-width: 3;
}

.spot-circle {
          fill: #b71c1c;
          cursor: pointer;
}

.spot-circle.selected {
          fill: #42b983;
}

.spot-node text {
          font-size: 12px;
          pointer-events: none;
}

.path-planning {
          padding: 20px;
          background: #fff;
          border-radius: 4px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.path-inputs {
          display: flex;
          gap: 10px;
          margin-bottom: 20px;
}

.spot-select {
          flex: 1;
          padding: 8px;
          border: 1px solid #ddd;
          border-radius: 4px;
}

.find-path-btn {
          padding: 8px 16px;
          background: #42b983;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
}

.find-path-btn:disabled {
          background: #ddd;
          cursor: not-allowed;
}

.path-steps {
          margin-top: 20px;
}

.path-step {
          display: flex;
          align-items: flex-start;
          margin-bottom: 10px;
}

.step-number {
          width: 24px;
          height: 24px;
          background: #42b983;
          color: white;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-right: 10px;
}

.step-content {
          flex: 1;
}

.distance {
          color: #666;
          font-size: 0.9em;
          display: block;
          margin-top: 4px;
}

.spot-list {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
          gap: 20px;
}

.spot-item {
          padding: 15px;
          background: #fff;
          border-radius: 4px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
          cursor: pointer;
}

.spot-item:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
</style>