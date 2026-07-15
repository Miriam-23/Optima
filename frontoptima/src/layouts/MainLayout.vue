<template>
  <v-app>

    <!-- TOP BAR -->
    <v-app-bar color="primary" elevation="2">
        <v-app-bar-nav-icon @click="drawer = !drawer" />

          <v-img :src="logo_dark" max-height="80" max-width="100" contain />

        <v-spacer />

        <v-btn icon @click="toggleTheme">
          <v-icon>{{ theme.global.name.value === 'light' ? 'mdi-white-balance-sunny' : 'mdi-weather-night' }}</v-icon>
        </v-btn>

        <v-btn icon>
            <v-icon>mdi-bell</v-icon>
        </v-btn>

        <v-btn icon @click="logout">
          <v-icon>mdi-logout</v-icon>
        </v-btn>
    </v-app-bar>

    <!-- SIDEBAR -->
    <v-navigation-drawer v-model="drawer" color="surface" app>     
      <!-- Perfil -->
      <!-- <div class="pa-5 text-center">

        <v-avatar size="80" color="primary">
          <v-img
            v-if="authStore.user?.avatar_url"
            :src="authStore.user.avatar_url"
          />

          <span
            v-else
            class="text-h5 font-weight-bold text-white"
          >
            {{ iniciales }}
          </span>
        </v-avatar>

        <div class="mt-3 text-subtitle-1 font-weight-bold">
          {{ authStore.user?.username }}
        </div>

        <div class="text-caption text-medium-emphasis">
          {{ authStore.user?.email }}
        </div>

      </div> -->

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

          <v-list-item-title>
            {{ authStore.user?.username }}
          </v-list-item-title>

          <v-list-item-subtitle>
            Mi perfil
          </v-list-item-subtitle>

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

  </v-app>
</template>

<script setup>
import logo_dark from '@/assets/images/logo_dark.png'
import Swal from 'sweetalert2'
import { ref } from 'vue'
import { useTheme } from 'vuetify'
import { defineEmits, defineProps } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { computed } from 'vue'

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
      background: 'rgba(0,0,0,0.6)',
      color: '#fff',
      backdrop: 'rgba(0,0,0,0.4)',
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

const theme = useTheme()

function toggleTheme() {
  theme.global.name.value =
    theme.global.name.value === 'light' ? 'dark' : 'light'
}

const emit = defineEmits(['toggleDrawer'])

const props = defineProps({
  drawer: {
    type: Boolean,
    default: false
  }
})

const drawer = ref(true)
</script>