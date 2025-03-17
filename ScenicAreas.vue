<template>
  <div class="scenic-areas-container">
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <span>正在加载...</span>
    </div>

    <div v-else class="scenic-areas-content">
      <h2>北京景区列表</h2>
      
      <div class="scenic-areas-grid">
        <div v-for="(coords, name) in landmarks" 
             :key="name" 
             class="scenic-area-card"
             @click="viewScenicArea(name, coords)">
          <h3>{{ name }}</h3>
          <div class="scenic-area-coords">
            <i class="fas fa-map-marker-alt"></i>
            <span>{{ formatCoords(coords) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ScenicAreas',
  data() {
    return {
      loading: false,
      landmarks: {
        '故宫': [116.397026, 39.918058],
        '天安门广场': [116.397390, 39.908710],
        '颐和园': [116.2755, 39.9988],
        '圆明园': [116.2984, 39.9994],
        '北海公园': [116.3845, 39.9263],
        '天坛': [116.4108, 39.8822],
        '景山公园': [116.3972, 39.9281],
        '什刹海': [116.3807, 39.9403],
        '南锣鼓巷': [116.4033, 39.9375],
        '国家大剧院': [116.3845, 39.9055],
        '鸟巢': [116.3903, 39.9929],
        '水立方': [116.3900, 39.9902],
        '798艺术区': [116.4950, 39.9843],
        '王府井': [116.4177, 39.9149],
        '前门大街': [116.3977, 39.8994]
      }
    }
  },
  methods: {
    formatCoords(coords) {
      return `经度: ${coords[0].toFixed(4)}, 纬度: ${coords[1].toFixed(4)}`;
    },
    viewScenicArea(name, coords) {
      this.$router.push({
        name: 'ScenicAreaDetail',
        params: { name },
        query: { 
          lat: coords[1],
          lng: coords[0]
        }
      }).catch(err => {
        if (err.name !== 'NavigationDuplicated') {
          console.error('导航错误:', err);
        }
      });
    }
  },
  async mounted() {
    try {
      this.loading = true;
      await new Promise(resolve => setTimeout(resolve, 500));
    } catch (error) {
      console.error('加载景区数据失败:', error);
    } finally {
      this.loading = false;
    }
  }
}
</script>

<style scoped>
.scenic-areas-container {
  padding: 20px;
  position: relative;
  min-height: 400px;
}

.scenic-areas-content {
  max-width: 1200px;
  margin: 0 auto;
}

.scenic-areas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.scenic-area-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.scenic-area-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.scenic-area-card h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.scenic-area-coords {
  color: #666;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 5px;
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
</style> 