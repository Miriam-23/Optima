import { defineStore } from 'pinia'
import api from '@/services/api'


function getStoredUser() {
  const user = localStorage.getItem('user')

  if (!user || user === 'undefined' || user === 'null') {
    return null
  }

  try {
    return JSON.parse(user)
  } catch (error) {
    console.error('Error leyendo usuario del localStorage:', error)
    localStorage.removeItem('user')
    return null
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: getStoredUser(),
    access: localStorage.getItem('access') || null,
    refresh: localStorage.getItem('refresh') || null,
  }),

  getters: { isAuthenticated: (state) => !!state.access,},

  actions: {

    async login(username, password) {
      try {
        const res = await api.post('/api/auth/login/', {
          username,
          password,
        })
        console.log(res.data)

        this.access = res.data.access
        this.refresh = res.data.refresh
        this.user = res.data.user

        localStorage.setItem('access', this.access)
        localStorage.setItem('refresh', this.refresh)
        localStorage.setItem('user', JSON.stringify(this.user))

        return true
      } catch (error) {
        console.log(error.response.data);
      }
    },

    // Registro
     async register(data) {
      try {
        const response = await api.post('/api/auth/register/', {
          username: data.username,
          email: data.email,
          password: data.password
        })

        return response.data

      } catch (error) {
        throw error.response?.data || error
      }
    },

    //CIERRE DE SESION
    async logout() {
      try {
        await api.post('/api/auth/logout/', {
          refresh: this.refresh
        })
      } catch (error) {
        console.error(error)
      } finally {
        this.user = null
        this.access = null
        this.refresh = null

        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        localStorage.removeItem('user')
      }
    }
  },
})
