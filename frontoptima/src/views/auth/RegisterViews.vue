<template>
  <v-container fluid class="login-wrapper pa-0">
    <v-row no-gutters class="fill-height">

      <!-- LADO IZQUIERDO -->
      <v-col
        cols="12"
        md="6"
        class="left-panel d-flex flex-column justify-center align-center"
      >

        <div class="text-center px-8">
          <v-img :src="logoLight" width="520" class="mx-auto" rounded="lg" />
        </div>

      </v-col>

      <!-- LADO DERECHO (REGISTRO) -->
      <v-col
        cols="12"
        md="6"
        class="right-panel d-flex justify-center align-center"
      >
        <v-card
          rounded="xl"
          elevation="10"
          width="550"
          class="login-card pa-8 text-white text-center"
          :style="{ backgroundColor: 'rgba(0, 0, 0, 0.5)', backdropFilter: 'blur(10px)' }"
        >

          <h2 class="mb-1">Crear cuenta</h2>

          <p class="mb-6 text-white">
            Regístrate para continuar
          </p>

          <!-- NOMBRE -->
          <v-text-field
            v-model="name"
            label="Usuario"
            prepend-inner-icon="mdi-account"
            variant="outlined"
          />

          <!-- EMAIL -->
          <v-text-field
            v-model="email"
            label="Correo electrónico"
            prepend-inner-icon="mdi-email"
            variant="outlined"
            class="mt-3"
          />
          <v-row>
            <!-- PASSWORD -->
            <v-col cols="12" md="6">
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
                    @click="showPassword = !showPassword"
                    class="cursor-pointer"
                  >
                    {{ showPassword ? 'mdi-eye-off' : 'mdi-eye' }}
                  </v-icon>
                </template>
              </v-text-field>
            </v-col>

            <!-- CONFIRM PASSWORD -->
            <v-col cols="12" md="6">
              <v-text-field
                v-model="confirmPassword"
                label="Confirmar contraseña"
                prepend-inner-icon="mdi-lock-check"
                :type="showPassword ? 'text' : 'password'"
                variant="outlined"
                class="mt-3"
              />
            </v-col>
          </v-row>
          <!-- BOTÓN -->
          <v-btn
            color="primary"
            block
            size="large"
            class="mt-4"
            :loading="loading"
            @click="register"
          >
            CREAR CUENTA
          </v-btn>

          <v-btn variant="text" 
            color="surface" 
            class="mt-2"
            @click="$router.push('/login')"
            >
            ¿Ya tienes cuenta? Inicia sesión
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
const authStore = useAuthStore()
const loading = ref(false)

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)

const register = async () => {

  if (!name.value || !email.value || !password.value || !confirmPassword.value) {

    Swal.fire({
      title: 'Error',
      text: 'Completa todos los campos',
      icon: 'error',
      background: 'rgba(0,0,0,0.6)',
      color: '#fff',
      timer: 1500,
      showConfirmButton: false
    })

    return
  }

  if (password.value.length < 8) {

    Swal.fire({
      title: 'Error',
      text: 'La contraseña debe tener mínimo 8 caracteres',
      icon: 'error',
      background: 'rgba(0,0,0,0.6)',
      color: '#fff',
      timer: 1500,
      showConfirmButton: false
    })

    return
  }

  if (password.value !== confirmPassword.value) {

    Swal.fire({
      title: 'Error',
      text: 'Las contraseñas no coinciden',
      icon: 'error',
      background: 'rgba(0,0,0,0.6)',
      color: '#fff',
      timer: 1500,
      showConfirmButton: false
    })

    return
  }

  loading.value = true

  try {

    await authStore.register({
      username: name.value,
      email: email.value,
      password: password.value
    })

    Swal.fire({
      title: 'Cuenta Creada',
      text:'Te enviamos un correo para activar tu cuenta.',
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

  } catch (error) {

    let mensaje = 'No fue posible crear la cuenta'

    if (error.response?.data) {

      const data = error.response.data

      if (typeof data === 'object') {
        mensaje = Object.values(data).flat().join('\n')
      }

    }

    Swal.fire({
      title: 'Error',
      text: mensaje,
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

  } finally {

    loading.value = false

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
