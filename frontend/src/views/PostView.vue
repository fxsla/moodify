<template>
  <nav class="navbar">
    <RouterLink to="/" class="logo">Moodify</RouterLink>

    <div class="nav-links" v-if="!authStore.isLoggedIn">
      <RouterLink to="/login" class="nav-button">Login</RouterLink>
      <RouterLink to="/signup" class="nav-button">Sign up</RouterLink>
    </div>

    <div class="user-info" v-if="authStore.isLoggedIn">
      <span class="user-level">
        Level: {{ Math.floor(authStore.user.xp / 100) }}
      </span>
      <span class="user-level">
        XP: {{ authStore.user.xp }}
      </span>
      <button @click="handleLogout" class="nav-button logout-button">Logout</button>
    </div>
  </nav>



  <div v-if="post" class="post-card">
    <div class="main-buttons">
      <RouterLink class="nav-button" to="/">Return</RouterLink>
      <button v-if="isOwner == true" class="delete-btn nav-button" @click="deletePost">Delete</button>
    </div>

    <div class="grouped-title">
        <h2 class="post-title">{{ post.title }}</h2>
        <p class="post-author">{{ post.author }} (Level {{ Math.floor(post.xp / 100) }})</p>
    </div>
    <p class="post-date">{{ formatTimestamp(post.created_at) }}</p>
    <p class="post-content">
      {{ post.content }}
    </p>
    <div v-if="authStore.isLoggedIn">
        <button  class="nav-button add-comment-btn" @click="modalInteract">Add comment</button>
    </div>
  </div>

  <div v-if="isModalVisible" class="modal">
    <div class="modal-content">
      <button @click="modalInteract" id="close-button">X</button>
      <h2>Create Comment</h2>
      <label for="content">Content:</label>
      <textarea id="content" v-model="newComment.content" required></textarea>
      <button @click="createComment(route.params.id)" id="submit-button">Reply</button>
    </div>
  </div>

  <div class="comment-card">
    <Comment v-for="comment in comments" :key="comment.id" :comment="comment" @delete-comment="deleteComment" ></Comment>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, RouterLink } from 'vue-router';
import { useAuthStore } from '../stores/user';
import Comment from '@/components/Comment.vue';
import router from '../router';

export default {
  name: 'PostView',
  components: {
    RouterLink,
    Comment,
  },

  setup() {
    const route = useRoute();
    const authStore = useAuthStore();
    const post = ref(null);
    const isModalVisible = ref(false);
    const newComment = ref({ content: '' });
    const comments = ref([])
    const isOwner = ref(false);

    const formatTimestamp = (timestamp) => {
      if (!timestamp) return 'Invalid Date';
      const date = new Date(timestamp);
      return date.toLocaleDateString([], {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    };

    const handleLogout = () => {
      authStore.logout();
    };

    const deleteComment = async (id) => {
      const response = await fetch(`http://localhost:8000/delete_comment/${id}/`,  {
            method: 'POST',
      });
      console.log(response)
      if(!response.ok){
        alert('Failed to delete')
      return;
      }
      
      fetchComments(route.params.id)

    }

    const modalInteract = () => {
      isModalVisible.value = !isModalVisible.value;
    };

    const fetchPost = async (id) => {
      try {
        const response = await fetch(`http://localhost:8000/posts/${id}`);
        if (!response.ok) {
          throw new Error('Failed to fetch post');
        }
        post.value = await response.json();

        if(authStore.user){
          if(authStore.user.is_superuser || authStore.user.username == post.value.author){
            isOwner.value = true;
          } else {
            isOwner.value = false;
          }
        } else {
          isOwner.value = false
        }
        
      } catch (error) {
        console.error(error);
        post.value = null;
      }
    };

    const deletePost = async () => {
      console.log(post.value.id)
       const response = await fetch(`http://localhost:8000/delete_post/${post.value.id}/`, {
            method: 'POST',
      });
      console.log(response)
      if(!response.ok){
        alert('Failed to delete')
        return;
      }

      alert('Successful! Returning to homepage')

      router.push('/');
  
    };
  
    const createComment = async (id) => {
      try {
        if(!newComment.value.content){
          console.log("cannot be empty")
          return;
        }

        console.log(id)
        const response = await fetch(`http://localhost:8000/comments/${id}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            post_id: id,
            content: newComment.value.content,
            user_id: authStore.user.id
          }),
        });

        if (!response.ok) {
          console.log("failed to add comment")
          return;
        }

        console.log('Comment created successfully');
        newComment.value.content = '';
        isModalVisible.value = false;

        authStore.add_xp(15)

        fetchComments(route.params.id)

      } catch (error) {
        console.log(error)
      }
    };

    const fetchComments = async (id) => {
      console.log(id)
      try {
        const response = await fetch(`http://localhost:8000/comments/${id}/`)

        if(!response.ok) {
          console.log('failed to fetch comments')
          return;
        }

        const data = await response.json()
        comments.value = data

        console.log(comments)

      } catch(error){
        console.log(error)
      }
    }


    onMounted(async () => {
      const postId = route.params.id;
      await fetchPost(postId);
      await fetchComments(postId);
    });

    return {
      route,
      post,
      comments,
      formatTimestamp,
      authStore,
      handleLogout,
      isModalVisible,
      modalInteract,
      newComment,
      createComment,
      isOwner,
      deletePost,
      deleteComment,
    };
  },
  
};
</script>

<style scoped>

.navbar {
  background-color: #1c2538;
  display: flex;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  margin-bottom:1rem;
  justify-content: space-between;
  padding: 1.5rem;
}

.logo {
  font-size: 1.8rem;
  font-weight: bold;
  color: rgb(255, 255, 255);
  text-decoration: none;
  margin: 0rem 10rem;
}

.nav-links, .user-info {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 1.5rem;
}

.nav-button:hover {
  background-color: rgb(163, 234, 42);
  color:#1c2538;
}

.nav-button {
  background-color: #1c2538;
  color: rgb(255, 255, 255);
  padding: 0.7rem 1.5rem;
  outline: none;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  text-decoration: none;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.welcome-message, .user-level {
  color: #eee;
  font-size: 1rem;
}

.user-level {
  font-weight: bold;
  color: rgb(163, 234, 42);
}

.logout-button {
  background-color: #b00f0f;
  color: #ffffff;
  border:none;
  font-weight: bold;
}

.logout-button:hover {
  background-color: #8b0202ed;
  color: #ffffff;
}
.navbar {
  background-color: #1c2538;
  display: flex;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  margin-bottom:1rem;
  justify-content: space-between;
  padding: 1.5rem;
}

.delete-btn {
  background-color: #b00f0f;
  outline: none;
  border: none;
}

.delete-btn:hover {
  background-color: #8b0202ed;
  color: #ffffff;
}

.post-card {
  background-color: white;
  padding: 2rem;
  margin: 2rem auto;
  max-width: 750px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  line-height: 1.6;
}


.post-title {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: #1c2538;
}

.grouped-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
}


.post-author {
  font-style: italic;
  color: #666;
  margin-bottom: 0.5rem;
  margin-top: none;
}

.post-date {
  color: #333;
  margin-top: 1.6rem;
  font-size: 1rem;
}

.main-buttons {
  display: flex;
  justify-content: space-between;
}

.post-content {
  color: #333;
  line-height: 1.7;
  background-color: #f3f3f3;
  overflow-wrap:break-word;
  padding:1.5rem;
  border-radius: 7px;
  margin-top: 2rem;
}

.add-comment-btn {
  width:100%;
  margin-left: auto;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  position: relative;
}

.modal-content h2 {
  margin-bottom: 1rem;
  color: #1c2538;
}

.modal-content label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: bold;
}

.modal-content textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 1rem;
  resize: vertical;
  min-height: 100px;
}

.modal-content button {
  padding: 0.75rem 1.5rem;
  background-color: #1c2538;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.modal-content button:hover {
  background-color: #141e30;
}

#close-button {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background-color: #b00f0f;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #ffffff;
}

#close-button:hover {
  color: white;
  background-color: #8b0202ed;
}

#submit-button {
  background-color: #1c2538;
  color: #FFFFFF;
  padding: 0.7rem 1.5rem;
  border: none;
  width: 100%;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease, box-shadow 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.textarea{
  height: 150px;
}

#submit-button:hover {
  background-color: rgb(163, 234, 42);
  color: #1c2538;
}


@media screen and (max-width:700px){
  .navbar {
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .user-info {
    flex-direction: column;
    width: 100%;
  }

  .logo {
    margin-right: 0;
    margin-left: 0;
  }

  .nav-links {
    margin-left: 0;
    width: 100%;
  }

  .logout-button {
    width: 100%;
    border-radius: 0;
  }

}

</style>
