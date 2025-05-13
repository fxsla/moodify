<template>
    <div class="login-container">
      <div class="login-card">
        <div class="title">
          <h3>Account Creation</h3>
          <p class="subtext">Moodify - A gamified social platform</p>
        </div>
  
        <form @submit.prevent="signup">
          <div class="form-group">
            <label for="username">Username</label>
            <input v-model="username" id="username" type="text" required />
          </div>
  
          <div class="form-group">
            <label for="email">Email</label>
            <input v-model="email" id="email" type="email" required />
          </div>
  
          <div class="form-group">
            <label for="password">Password</label>
            <input v-model="password" id="password" type="password" required />
          </div>
  
          <button type="submit" id="sign-up-btn">Sign Up</button>
        </form>
  
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
  
        <p class="bottomtext">Already have an account? <RouterLink to="/login" class="signup">Log in</RouterLink>.</p>
        <p class="bottomtext"> Back to <RouterLink to="/" class="signup">Home</RouterLink>.</p>
      </div>
    </div>
</template>
  
<script>
    export default {
        name: 'SignupView',
        data() {
            return {
                username: '',
                email: '',
                password: '',
                error: null,
            };
        },
        methods: {
            async signup() {
                this.error = null;
        
                try {
                const response = await fetch('http://localhost:8000/signup/', {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: this.username,
                        email: this.email,
                        password: this.password,
                    }),
                });

                await response.json(); 
        
                if (!response.ok) {
                    this.error = 'Username or password incorrect';
                    return; 
                }
        
                this.$router.push('/login');
        
                } catch (err) {
                    console.log(err)
                }
            },
        },
    };
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
        font-weight: bold;
    }
    
    h3 {
        margin-bottom: 0;
    }
    
    input {
        outline: none;
    }
    
    input:focus {
        border-color: rgb(163, 234, 42);
    }
    
    .login-card {
        background-color: white;
        padding: 3rem;
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
        background-color: rgb(163, 234, 42);
        border-color: rgb(163, 234, 42);
        color: rgb(21, 28, 43);
        border-radius: 2px;
        cursor: pointer;
        margin-top: 1rem;
    }
    
    button:hover {
        background-color: rgba(163, 234, 42, 0.3);
    }
    
    .error-message {
        margin: 0rem;
        color: red;
        text-align: center;
    }
</style>