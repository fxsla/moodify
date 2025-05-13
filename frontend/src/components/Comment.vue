<template>
  <div class="comment">
    <p class="comment-author">
      <strong>{{ comment.author }} (Level {{ Math.floor(comment.xp/100) }})</strong> 
      <button v-if="isOwner" class="delete-btn" @click="deleteComment">Remove</button>
    </p>
    <p class="comment-content">{{ comment.content }}</p>
    <p class="comment-date">
      Posted on: {{ comment.created_at }}
    </p>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/user';

export default {

  name: 'Comment',
  props: {
    comment: {
      type: Object,
      required: true,
    },
    post: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
        isOwner: false,
    }
  },

  methods: {
    checkIfAdmin(){
      if (this.authStore.user) { // Make sure user exists
        if (this.comment.author === this.authStore.user.username) {
          console.log(this.comment.author, this.authStore.user.username)
          this.isOwner = true;
        } else if (this.authStore.user.is_superuser === true) {
          console.log(this.authStore.user.is_superuser)
          this.isOwner = true;
        }
      }
    },

    deleteComment() {
      this.$emit('delete-comment', this.comment.id);
    },
  },


  setup(){
    const authStore = useAuthStore();

    return {
      authStore,
    }
  },

  mounted() {
    this.checkIfAdmin()
  }

};

</script>



<style>

.comment {
  background-color: #f8f9fa;
  border: 1px solid #e2e3e4; 
  border-radius: 5px;
  padding: 0.9rem 2rem;
  margin-bottom: 1rem; 
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease-in-out;
  max-width: 750px;
  margin: 0 auto;
  margin-top:0.8rem;
  margin-bottom: 0.8rem;
}

.delete-btn {
  padding: 0.3rem 0.5rem;
}

.delete-btn {
  background-color: #343a40;
  color: #ffffff;
  border: none;
  border-radius: 3px;
}

.delete-btn:hover {
  background-color: #8b0202ed;
  color: #ffffff;
  cursor:pointer;
}

.comment-author {
  font-size: 0.75rem;
  color: #6c757d;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-date {
  font-size: 0.7rem;
  color: #999;
  margin-bottom: 0.1rem;
}

.comment-content {
  font-size: 0.9rem;
  line-height: 1.4;
  color: #343a40;
  overflow:hidden;
}


</style>