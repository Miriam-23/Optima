<template>
  <v-app>

    <!-- TOP BAR -->
    <v-app-bar color="primary" elevation="2">
      <!-- BOTON DRAWER -->
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-img :src="icono_dark" max-height="40" max-width="40" contain />
      <span class="logo-text">OPTIMA</span>

      <v-spacer />

      <!-- BOTON DE NOTIFICCIONES -->
      <NotificationsMenu />

      <!-- BOTON DE TEMA -->
      <v-btn icon @click="toggleTheme">
        <v-icon>{{ theme.global.name.value === 'light' ? 'mdi-white-balance-sunny' : 'mdi-weather-night' }}</v-icon>
      </v-btn>

      <!-- BOTON CIERRE DE SESION -->
      <v-btn icon @click="logout">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- SIDEBAR -->
    <v-navigation-drawer v-model="drawer" color="surface" app>     
      
      <v-divider /> 

      <!-- MODULOS DE NAVEGACIÓN -->
      <v-list nav>
        <!-- Perfil -->
        <v-list-item to="/perfil">
          <template #prepend>
            <v-avatar size="40" color="primary">
              <v-img
                v-if="authStore.user?.avatar_url"
                :src="authStore.user.avatar_url"
              />
              <span v-else class="text-caption font-weight-bold text-white">
                {{ iniciales }}
              </span>
            </v-avatar>
          </template>

          <v-list-item-title> {{ authStore.user?.username }} </v-list-item-title>

          <v-list-item-subtitle>Mi perfil</v-list-item-subtitle>

        </v-list-item>
        <v-list-item to="/dashboard" prepend-icon="mdi-view-dashboard" title="Dashboard" />
        <v-list-item to="/proyectos" prepend-icon="mdi-folder" title="Proyectos" />
        <v-list-item to="/tareas" prepend-icon="mdi-format-list-checkbox" title="Tareas" />

      </v-list>
    </v-navigation-drawer>

    <!-- CONTENIDO -->
    <v-main class="bg-background">
      <v-container fluid class="pa-6">
        <router-view />
      </v-container>
    </v-main>
    
    <!-- BOTON DE CHATBOT -->
    <ChatBotButton />

  </v-app>
</template>

<script setup>
import icono_dark from '@/assets/icons/icono_dark.png'
import Swal from 'sweetalert2'
import { ref } from 'vue'
import { useTheme } from 'vuetify'
import { defineEmits, defineProps } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { computed } from 'vue'
import NotificationsMenu from '@/components/notifications/NotificationsMenu.vue'
import ChatBotButton from '@/components/chatbot/ChatBotButton.vue'

const theme = useTheme()
const isDark = theme.global.current.value.dark
const authStore = useAuthStore()
const router = useRouter()

//PENDIENTE POR VERIFICAR SI EL BACKEND DEVUELVE FOTO
const iniciales = computed(() => {
  const nombre = authStore.user?.username || 'U'
  return nombre
    .split(' ')
    .map(n => n[0])
    .join('')
    .substring(0, 2)
    .toUpperCase()
})

const logout = async () => {
  try {
    await authStore.logout()

    Swal.fire({
      icon: 'success',
      title: 'Sesión cerrada',
      text: 'Hasta pronto',
      background: isDark ? "#1E1E1E" : "#FFFFFF",
      color: isDark ? "#F5F5F5" : "#1F2937",
      backdrop: isDark ? "rgba(0,0,0,.75)" : "rgba(0,0,0,.45)",
      showConfirmButton: false,
      timer: 1200,
      timerProgressBar: false,
      customClass: {
        popup: 'swal2-glass'
      }
    })
  } finally {
    router.push('/login')
  }
}

const toggleTheme = () => {
  theme.change(
    theme.global.current.value.dark ? "light" : "dark"
  )
}

const emit = defineEmits(['toggleDrawer'])

const props = defineProps({
  drawer: {
    type: Boolean,
    default: false
  }
})

const drawer = ref(false)
</script>

<style scoped>
.logo-text {
  font-size: 1.6rem;
  font-weight: 700;
  font-family: 'Poppins', sans-serif;
  color: white; /* Cambia a black si tu AppBar es clara */
  letter-spacing: 1px;
}
</style>