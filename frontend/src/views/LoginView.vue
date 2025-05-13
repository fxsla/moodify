<template>
    <div class="login-container">
        <div class="login-card">
            <div class="title">
                <h3>Welcome back!</h3>
                <p class="subtext">Log in to your account.</p>
            </div>

            <form @submit.prevent="handleLogin">

                <div class="form-group">
                    <label for="username">Username</label>
                    <input v-model="username" id="username" type="text" required/>
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input v-model="password" id="password" type="password" required/>
                </div>
                <button type="submit" id="log-in-btn">Log In</button>
            </form>

            <p class="bottomtext"> Don't have an account? <RouterLink to="/signup" class="signup">Sign up</RouterLink>.</p>
            <p class="bottomtext"> Back to <RouterLink to="/" class="signup" id="home">Home</RouterLink>.</p>
        </div>
    </div>
</template>
  
<script>
import { useAuthStore } from '@/stores/user'

export default {
    name: 'Login',
    data() {
        return {
            username: '',
            password: '',
            error: null,
        }
    },
    methods: {
        async handleLogin() {
            try {
            this.error = null;
            const authStore = useAuthStore();
            await authStore.login(this.username, this.password)
            } catch (err) {
                this.error = "Username or password incorrect."
            }
        }
    }
}
</script>
  
<style scoped>

    .login-container {
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f2f2f2;
    }

    .subtext {
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    .bottomtext {
        margin-top: 2rem;
    }

    .signup {
        color: rgb(163, 234, 42);
        font-weight:bold;
    }

    h3 {
        margin-bottom:0;
    }

    input {
        outline:none;
    }

    input:focus {
        border-color: rgb(163, 234, 42);
        
    }

    .login-card {
        background-color: white;
        padding: 3rem 3rem 3rem 3rem;
        width: 100%;
        max-width: 550px;
        border-radius: 3px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    }
    
    .title {
        font-size: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .form-group {
        margin-bottom: 2.5rem;
        display: flex;
        flex-direction: column;
    }
    
    label {
        margin-bottom: 0.25rem;
    }
    
    input {
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    
    button {
        width: 100%;
        padding: 0.5rem;
        background-color:rgb(163, 234, 42);
        border-color:rgb(163, 234, 42);
        color: rgb(21, 28, 43);
        border-radius: 2px;
        cursor: pointer;
        margin-top: 1rem;
    }
    
    button:hover {
        background-color: rgba(163, 234, 42, 0.3);
    }
    
</style>
  