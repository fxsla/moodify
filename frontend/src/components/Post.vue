<template>
  <div class="post-card" id="post-item">

    <h2 class="post-title">{{ post.title }}</h2>
    <p class="post-author">{{ post.author }} (Level {{ Math.floor(post.xp/100)  }})</p>
    
    <p class="post-date">
      {{ formatTimestamp(post.created_at) }}
    </p>

    <p class="post-content">
      {{ post.content }}
    </p>

  </div>
</template>

<script>


export default {
name: 'Post',
props: {
post: {
    type: Object,
    required: true,
    },
},
data() {
  return {
    xp: 0,
  }
},


methods: {
    formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleDateString(
        [],
        {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        },
        );
        },
    },
}


</script>

<style scoped>


.post-card {
  background-color: #f8f9fa;
  border: 1px solid #e2e3e4; 
  border-radius: 5px;
  padding: 0.5rem 2rem;
  margin-bottom: 1rem; 
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease-in-out;
  max-width: 900px;
  min-width: 450px;
  margin: 0 auto;
}


.post-card:hover {
  border-color: #b8daff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  cursor: pointer;
}
.post-title {
  font-size: 1.25rem;
  margin-bottom: 0.1rem;
  color: #2c3e50;
  font-weight: bold;
}


.post-author {
  font-size: 0.75rem;
  color: #6c757d;
  margin-bottom: 0rem;
}

.post-date {
  font-size: 0.7rem;
  color: #999;
  margin-bottom: 0.1rem;
}


.post-content {
  font-size: 0.9rem;
  line-height: 1.4;
  color: #343a40;
  overflow:hidden;
}

</style>
