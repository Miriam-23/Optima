<template>
  <v-container fluid class="login-wrapper pa-0">
    <v-row no-gutters class="fill-height">

      <!-- Lado izquierdo -->
      <v-col
        cols="12"
        md="6"
        class="left-panel d-flex flex-column justify-center align-center"
      >
        <div class="text-center px-8">
          <v-img
            :src="logoLight"
            width="520"
            class="mx-auto"
            rounded="lg"
          />
        </div>
      </v-col>

      <!-- Lado derecho -->
      <v-col
        cols="12"
        md="6"
        class="right-panel d-flex justify-center align-center"
      >

        <v-card
          rounded="xl"
          elevation="10"
          class="login-card pa-8 text-white text-center"
          :style="{
            backgroundColor: 'rgba(0,0,0,0.5)',
            backdropFilter: 'blur(10px)'
          }"
        >
        
        <!-- Mensaje estado de verificación de cuenta (Cargando) -->
        <div v-if="estado === 'loading'">
            <v-progress-circular
                indeterminate
                color="primary"
                size="70"
                class="mb-6"
            />

            <h2 class="mb-2">
                Verificando tu cuenta...
            </h2>

            <p class="text-white">
                Esto solo tomará unos segundos.
            </p>
        </div>

        <!-- Mensaje estado de verificación de cuenta (Exito) -->
        <div v-else-if="estado === 'success'">
            <v-icon
                color="success"
                size="80"
                class="mb-5"
            >
                mdi-check-circle
            </v-icon>

            <h2 class="mb-3">
                ¡Cuenta verificada!
            </h2>

            <p class="text-white mb-6">
                {{ mensaje }}
            </p>

            <RouterLink to="/login">

                <v-btn
                color="primary"
                block
                >
                Ir al inicio de sesión
                </v-btn>

            </RouterLink>
        </div>

        <!-- Mensaje estado de verificación de cuenta (Error) -->
        <div v-else>
            <v-icon
                color="error"
                size="80"
                class="mb-5"
            >
                mdi-close-circle
            </v-icon>

            <h2 class="mb-3">
                No pudimos verificar tu cuenta
            </h2>

            <p class="text-white mb-6">
                {{ mensaje }}
            </p>

            <RouterLink to="/register">

                <v-btn
                color="primary"
                block
                >
                Volver al registro
                </v-btn>

            </RouterLink>
        </div>

        </v-card>

      </v-col>

    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'
import logoLight from '@/assets/images/logo_ligth.png'

const route = useRoute()

const estado = ref('loading')
// loading | success | error

const mensaje = ref('')

const verificarCuenta = async () => {

  const token = route.params.token

  try {

    const response = await api.get(`/api/auth/verificar/${token}/`)

    estado.value = 'success'
    mensaje.value = response.data.mensaje

  } catch (error) {

    estado.value = 'error'

    if (error.response?.data?.mensaje) {
      mensaje.value = error.response.data.mensaje
    } else {
      mensaje.value = 'No fue posible verificar la cuenta.'
    }

  }

}

onMounted(() => {
  verificarCuenta()
})
</script>

<style scoped>
.login-wrapper {
  height: 100vh;
}

.left-panel {
  background-image: url("@/assets/images/gestor.jpeg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.right-panel {
  background: linear-gradient(135deg, #60bcfa, #073291);
}

.login-card {
  width: 100%;
  max-width: 420px;
}
</style>