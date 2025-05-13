<template>
  <nav class="navbar">
    <RouterLink to="/" class="logo">Moodify</RouterLink>
    
    <div class="nav-links" v-if="!authStore.isLoggedIn">
      <RouterLink to="/login" class="nav-button">Login</RouterLink>
      <RouterLink to="/signup" class="nav-button">Sign up</RouterLink>
    </div>
    
    <div class="user-info" v-if="authStore.isLoggedIn">
      <span class="welcome-message">
        Hello, {{ authStore.user.username }}!
      </span>
      <span class="user-level">
        Level: {{ Math.floor(authStore.user.xp / 100) }}
      </span>
      <span class="user-level">
        XP: {{ authStore.user.xp }}
      </span>
      <button @click="handleLogout" class="nav-button logout-button">Logout</button>
    </div>
  </nav> 
  <div class="main-body">
    <button @click="modalInteract" class="create-post-btn special">Create Post</button>
    <Post class="flex-item" v-for="post in posts" :key="post.id" :post="post" @click="openPost(post.id)"></Post>
  </div>

  <div v-if="isModalVisible" class="modal">
    <div class="modal-content">
      <button @click="modalInteract" id="close-the-modal">X</button>
      <h2>Create Post</h2>

      <label for="title">Title:</label>
      <input type="text" id="title" v-model="newPost.title" required>

      <label for="content">Content:</label>
      <textarea id="content" v-model="newPost.content" required></textarea>

      <button class="submit-post-btn" @click="createPost">Post</button>
    </div>
  </div>
        
</template>

<script>
import Post from '@/components/Post.vue';
import { useAuthStore } from '../stores/user'
import { RouterLink } from 'vue-router';

export default {
  name:'HomeView',
  components: {
    RouterLink,
    Post,
  },
  data() {
    return {
      isModalVisible: false,
      newPost: {
        title: '',
        content: '',
      },
      posts: [],
    }
  },

  methods: {

    openPost(id) {
      this.$router.push({ 
      name: 'PostDetails',
      params: { id: id },
      });
      console.log("Worked?");
    },
    modalInteract() 
    {
      this.isModalVisible = !this.isModalVisible
    },

    async createPost() 
    {
      try {
        if(!this.newPost.title){
          console.log("Please enter a valid title")
        }

        if(!this.newPost.content){
          console.log("Please enter valid content")
        }

        const response = await fetch('http://localhost:8000/post/', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            author: this.authStore.user.username,
            title: this.newPost.title,
            content: this.newPost.content,
          }),
        });

        if(!response.ok) {
          throw new Error('failed to create post')
        }

        this.authStore.add_xp(25)
        const data = await response.json()
        this.posts.unshift(data)
        this.modalInteract()

        this.newPost = {
          title: '', 
          content: '',
        }

        this.fetchPosts()

      }catch (error){
        console.error(error);
      }
    },

    async fetchPosts()
    {
      try{
        const response = await fetch('http://localhost:8000/posts/')

        if(!response.ok){
          throw new Error('failed to fetch posts')
        }
        
        const data = await response.json()
        this.posts = data
        
        console.log(this.posts)

      } catch(error){
        console.log(error)
      }
    },
  },

  setup(){
    const authStore = useAuthStore();

    const handleLogout = () => {
      authStore.logout()
    }

    return {
      authStore,
      handleLogout
    }

  },
  mounted() {
    this.fetchPosts();
  }

}
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
  margin: 0rem 5rem;
}

.create-post-btn {
  padding: 0.8rem 4rem;
  outline: none;
  border: 1px solid rgb(163, 234, 42);
  border-radius: 3px;
  background-color: rgb(163, 234, 42);
}

.create-post-btn:hover{
  background-color: #1c2538;
  color: white;
  transition: 0.3s;
  cursor: pointer;
}


.submit-post-btn {
  width:100%;
  margin-top:1.5rem;
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
  border: 1.6px solid rgb(163, 234, 42);
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
.navbar {
  background-color: #1c2538;
  display: flex;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  margin-bottom:1rem;
  justify-content: space-between;
  padding: 1.5rem;
}
.logout-button:hover {
  background-color: #8b0202ed;
  color: #ffffff;
}

.main-body {
  display:flex;
  flex-direction: column;
  margin: 0 auto;
  align-items: center;
  gap: 0.6rem;
}

.flex-item {
  width: 50%;
}

.modal {
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items:center;
  justify-content: center;
}

.modal-content {
  background-color: white;
  color: #333;
  padding: 2rem;
  border-radius: 10px;
  max-width: 600px;
  width: 95%;
  position: relative;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.modal-content h2 {
  color: #1c2538;
}

.modal-content label {
  display: block;
  margin-top: 1rem;
  color: #1c2538;
}

.modal-content input, .modal-content textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #1c2538;
  border-radius: 4px;
  margin-top: 0.5rem;
  resize: none;
  font-size: 1rem;
}

.modal-content input:focus, .modal-content textarea:focus {
  outline: none;
  border: 1px solid rgb(163, 234, 42);
}

.modal-content textarea {
  height: 150px;
}

.modal-content button {
  padding: 0.75rem 1.5rem;
  background-color: #1c2538;
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.modal-content button:hover {
  background-color: rgb(163, 234, 42);
  border:1px solid rgb(163, 234, 42);
  transition: 0.3s;
}

.close-button {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  font-size: 1rem;
  cursor: pointer;
  background: none;
  border: none;
  color: #1c2538;
}

@media screen and (max-width:1000px){
  .welcome-message {
    display:none;
  }
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
