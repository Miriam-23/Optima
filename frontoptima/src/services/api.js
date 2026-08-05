import axios from 'axios'

// La URL del backend viene de la variable de entorno VITE_API_URL.
// En local sale de frontoptima/.env; en Vercel se define en
// Settings > Environment Variables. El fallback es solo para desarrollo.
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL,
})

// Interceptor para token automático
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

export default api