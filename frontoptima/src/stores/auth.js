import { defineStore } from 'pinia'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    access: localStorage.getItem('access') || null,
    refresh: localStorage.getItem('refresh') || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.access,
  },

  actions: {

    async login(email, password) {
      try {
        const res = await api.post('/api/auth/login/', {
          email,
          password,
        })

        this.access = res.data.access
        this.refresh = res.data.refresh
        this.user = res.data.user

        localStorage.setItem('access', this.access)
        localStorage.setItem('refresh', this.refresh)
        localStorage.setItem('user', JSON.stringify(this.user))

        return true
      } catch (error) {
        console.error('Error login:', error)
        return false
      }
    },

    logout() {
      this.user = null
      this.access = null
      this.refresh = null

      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      localStorage.removeItem('user')
    },
  },
})