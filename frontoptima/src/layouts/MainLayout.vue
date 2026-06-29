<template>
  <v-app>

    <!-- TOP BAR -->
    <v-app-bar color="primary" elevation="2">
        <v-app-bar-nav-icon @click="drawer = !drawer" />
        
        <v-toolbar-title class="d-flex align-center">
            <v-icon max-height="40" max-width="40">
                <v-img :src="icono_dark" />
            </v-icon>
            OptimaPM
        </v-toolbar-title>
        <!-- <v-toolbar-title class="d-flex align-center">
            <v-icon max-height="60" max-width="80">
                <v-img :src="logo_dark" />
            </v-icon>
        </v-toolbar-title> -->

        <v-spacer />

        <v-btn icon @click="toggleTheme">
          <v-icon>{{ theme.global.name.value === 'light' ? 'mdi-white-balance-sunny' : 'mdi-weather-night' }}</v-icon>
        </v-btn>

        <v-btn icon>
            <v-icon>mdi-bell</v-icon>
        </v-btn>

        <v-btn icon>
            <v-icon>mdi-account-circle</v-icon>
        </v-btn>
        <v-btn icon @click="logout">
          <v-icon>mdi-logout</v-icon>
        </v-btn>
    </v-app-bar>

    <!-- SIDEBAR -->
    <v-navigation-drawer v-model="drawer" app>
      <v-list nav>

        <v-list-item to="/dashboard" prepend-icon="mdi-view-dashboard" title="Dashboard" />
        <v-list-item to="/proyectos" prepend-icon="mdi-folder" title="Proyectos" />
        <v-list-item to="/tareas" prepend-icon="mdi-format-list-checkbox" title="Tareas" />
        <v-list-item to="/usuarios" prepend-icon="mdi-account-group" title="Usuarios" />
        <v-list-item to="/reportes" prepend-icon="mdi-chart-box" title="Reportes" />
        <v-list-item to="/configuracion" prepend-icon="mdi-cog" title="Configuración" />

      </v-list>
    </v-navigation-drawer>

    <!-- CONTENIDO -->
    <v-main class="bg-grey-lighten-4">
      <v-container fluid class="pa-6">
        <router-view />
      </v-container>
    </v-main>

  </v-app>
</template>

<script setup>
import icono_dark from '@/assets/icons/icono_dark.png'
import logo_dark from '@/assets/images/logo_dark.png'
import { ref } from 'vue'
import { useTheme } from 'vuetify'
import { defineEmits, defineProps } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const logout = () => {
  auth.logout()
  router.push('/login')
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