<template>
  <div class="scenic-area-list">
    <h2>中国文化景区</h2>
    
    <div v-if="loading" class="loading">
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>
    
    <div v-else class="area-grid">
      <div 
        v-for="(area, id) in scenicAreas" 
        :key="id"
        class="area-card"
        @click="goToArea(id)"
      >
        <div class="card-image" :style="`background-image: url('https://images.unsplash.com/photo-1584646098378-0874589d76b1?q=80&w=800')`"></div>
        <div class="card-content">
          <h3>{{ area.name }}</h3>
          <p>景点数量: {{ area.spot_count }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ScenicAreaList',
  data() {
    return {
      scenicAreas: {},
      loading: true,
      error: null
    };
  },
  created() {
    this.fetchScenicAreas();
  },
  methods: {
    async fetchScenicAreas() {
      try {
        this.loading = true;
        const response = await axios.get('/api/scenic_areas');
        this.scenicAreas = response.data;
        this.loading = false;
      } catch (error) {
        console.error('Error fetching scenic areas:', error);
        this.error = '获取景区数据失败，请稍后再试';
        this.loading = false;
      }
    },
    goToArea(id) {
      this.$router.push(`/scenic-areas/${id}`);
    }
  }
}
</script>

<style scoped>
.scenic-area-list {
  max-width: 1200px;
  margin: 0 auto;
}

.scenic-area-list h2 {
  text-align: center;
  margin-bottom: 2rem;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
}

.area-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.area-card {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.area-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.card-image {
  height: 200px;
  background-size: cover;
  background-position: center;
}

.card-content {
  padding: 1.5rem;
}

.card-content h3 {
  margin-top: 0;
  margin-bottom: 0.5rem;
}
</style> 