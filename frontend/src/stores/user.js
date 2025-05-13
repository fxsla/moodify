import { defineStore } from 'pinia';
import router from '../router';


export const useAuthStore = defineStore('auth', {
    state: () => ({
        isLoggedIn: localStorage.getItem('isLoggedIn') === 'true',
        user: JSON.parse(localStorage.getItem('user') || null),
    }),
    actions: {
        async login(username, password) {
            try {
                const response = await fetch('http://localhost:8000/login/', {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({username, password}),
                })

                const data = await response.json();

                if(!response.ok){
                    alert("Incorrect username or password!")
                    throw new Error('Login failed')
                }

                this.isLoggedIn = true
                this.user = {
                    id: data.id,
                    username: data.username,
                    xp: data.xp,
                    is_superuser: data.is_superuser,
                }

                localStorage.setItem('isLoggedIn', 'true');
                localStorage.setItem('user', JSON.stringify(this.user))
                router.push('/')

            } catch (error) {
                console.log(error)
            }
        },

        async logout() {
            try {
                const response = await fetch('http://localhost:8000/logout/', {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                })

                if (!response.ok) {
                    throw new Error('Logout failed')
                }

                this.isLoggedIn = false
                this.user = null

                localStorage.removeItem('isLoggedIn')
                localStorage.removeItem('user')
                
                router.push('/');
            } catch(error){
                console.log(error)
            }
        },

        async add_xp(xpToAdd) {
            try {
                const response = await fetch('http://localhost:8000/xp/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        id:this.user.id,
                        xp:xpToAdd,
                    })
                })

                if (!response.ok) {
                    throw new Error('failed to update xp')
                }

                this.user.xp += xpToAdd;
                localStorage.setItem('user', JSON.stringify(this.user));
            } catch (error) {
                console.log(error)
            }

        },
    }
})

