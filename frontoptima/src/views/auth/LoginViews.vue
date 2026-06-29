<template>
  <v-container fluid class="login-wrapper pa-0">
    <v-row no-gutters class="fill-height">

      <!-- LADO IZQUIERDO (branding / ilustración) -->
      <v-col
        cols="12"
        md="6"
        class="left-panel d-flex flex-column justify-center align-center"
      >
        <div class="text-center px-8">
          <v-img :src="logoLight" width="520" class="mx-auto" rounded="lg" />
        </div>
      </v-col>

      <!-- LADO DERECHO (formulario) -->
      <v-col
        cols="12"
        md="6"
        class="right-panel d-flex justify-center align-center"
      >
        <v-card rounded="xl" elevation="10" class="login-card pa-8 text-white text-center align-center" 
          :style="{backgroundColor: 'rgba(0, 0, 0, 0.5)', backdropFilter: 'blur(10px)' }"
        >
          <h2 class="mb-1 justify-center">Bienvenido</h2>
          <p class="mb-6 text-white">
            Inicia sesión para continuar
          </p>

          <!-- EMAIL -->
          <v-text-field
            v-model="email"
            label="Correo electrónico"
            prepend-inner-icon="mdi-email"
            variant="outlined"
          />

          <!-- PASSWORD -->
          <v-text-field
            v-model="password"
            label="Contraseña"
            prepend-inner-icon="mdi-lock"
            :type="showPassword ? 'text' : 'password'"
            variant="outlined"
            class="mt-3"
          >
            <template #append-inner>
              <v-icon
                class="cursor-pointer"
                @click="showPassword = !showPassword"
              >
                {{ showPassword ? 'mdi-eye-off' : 'mdi-eye' }}
              </v-icon>
            </template>
          </v-text-field>

          <!-- OPCIONES -->
          <div class="d-flex justify-space-between align-center mt-2">
            <v-checkbox
              v-model="remember"
              label="Recordarme"
              density="compact"
              hide-details
            />

          </div>

          <!-- BOTÓN -->
          <v-btn
            color="primary"
            block
            size="large"
            class="mt-2 mb-2"
            :loading="loading"
            @click="login"
          >
            Iniciar sesión
          </v-btn>

          <v-btn variant="text" color="surface" @click="$router.push('/register')">
            CREAR CUENTA
          </v-btn>

          <v-btn variant="text" color="surface">
            ¿Olvidaste tu contraseña?
          </v-btn>
        </v-card>
      </v-col>

    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import logoLight from '@/assets/images/logo_ligth.png'
import Swal from 'sweetalert2'

const router = useRouter()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const remember = ref(false)
const showPassword = ref(false)
const loading = ref(false)

const login = async () => {
  loading.value = true

  const success = await auth.login(email.value, password.value)

  loading.value = false

  if (success) {
    Swal.fire({
      title: 'Exito!',
      text: 'Inicio de Sesión exitoso',
      icon: 'success',
      background: 'rgba(0,0,0,0.6)',
      color: '#fff',
      backdrop: 'rgba(0,0,0,0.4)',
      showConfirmButton: false,
      timer: 1500,
      timerProgressBar: false,
      customClass: {
        popup: 'swal2-glass'
      }
    })
    router.push('/dashboard')
  } else {
     Swal.fire({
      title: 'Error!',
      text: 'Credenciales incorrectas',
      icon: 'error',
      background: 'rgba(0,0,0,0.6)',
      color: '#fff',
      backdrop: 'rgba(0,0,0,0.4)',
      showConfirmButton: false,
      timer: 1500,
      timerProgressBar: false,
      customClass: {
        popup: 'swal2-glass'
      }
    })
  }
}
</script>

<style scoped>
.login-wrapper {
  height: 100vh;
}

/* Panel izquierdo */
.left-panel {
  background-image: url("@/assets/images/gestor.jpeg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* Panel derecho */
.right-panel {
  background: linear-gradient(135deg, #60bcfa, #073291);
}

/* Card del login */
.login-card {
  width: 100%;
  max-width: 420px;
  border-radius: 16px;
}
</style>