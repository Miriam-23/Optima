<template>
  <v-container fluid class="login-wrapper pa-0">
    <v-row no-gutters class="fill-height">

      <!-- Panel izquierdo -->
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

      <!-- Panel derecho -->
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
            backgroundColor: 'rgba(0,0,0,.5)',
            backdropFilter: 'blur(10px)'
          }"
        >

        <!-- FORMULARIO -->
        <div v-if="estado === 'form'">

          <v-icon
            color="primary"
            size="80"
            class="mb-5"
          >
            mdi-lock-reset
          </v-icon>

          <h2 class="mb-2">
            Recuperar contraseña
          </h2>

          <p class="text-white mb-6">
            Ingresa el correo asociado a tu cuenta.
            Si está registrado, recibirás un enlace para restablecer tu contraseña.
          </p>

          <v-form
            ref="form"
            @submit.prevent="enviarEnlace"
          >

            <v-text-field
              v-model="email"
              label="Correo electrónico"
              prepend-inner-icon="mdi-email"
              variant="outlined"
              :rules="emailRules"
            />

            <v-btn
              color="primary"
              block
              :loading="loading"
              type="submit"
            >
              Enviar enlace
            </v-btn>

          </v-form>

          <RouterLink
            to="/login"
            class="text-decoration-none"
          >
            <v-btn
              variant="text"
              color="white"
              class="mt-4"
            >
              Volver al inicio de sesión
            </v-btn>
          </RouterLink>

        </div>

        <!-- ÉXITO -->
        <div v-else-if="estado === 'success'">

          <v-icon
            color="success"
            size="80"
            class="mb-5"
          >
            mdi-email-check
          </v-icon>

          <h2 class="mb-3">
            ¡Correo enviado!
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

        <!-- ERROR -->
        <div v-else-if="estado === 'error'">

          <v-icon
            color="error"
            size="80"
            class="mb-5"
          >
            mdi-email-remove
          </v-icon>

          <h2 class="mb-3">
            No fue posible enviar el correo
          </h2>

          <p class="text-white mb-6">
            {{ mensaje }}
          </p>

          <v-btn
            color="primary"
            block
            @click="estado='form'"
          >
            Intentar nuevamente
          </v-btn>

        </div>

        </v-card>

      </v-col>

    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue"
import authService from "@/services/auth.service"
import logoLight from "@/assets/images/logo_ligth.png"

const form = ref()

const estado = ref("form")
const email = ref("")
const mensaje = ref("")
const loading = ref(false)

const emailRules = [
  v => !!v || "El correo es obligatorio.",
  v => /.+@.+\..+/.test(v) || "Correo inválido."
]

const enviarEnlace = async () => {

  const { valid } = await form.value.validate()

  if (!valid) return

  loading.value = true

  try {

    const response = await authService.forgotPassword(email.value)

    mensaje.value = response.data.mensaje

    estado.value = "success"

  } catch (error) {

    mensaje.value =
      error.response?.data?.mensaje ||
      error.response?.data?.error ||
      "No fue posible enviar el correo. Inténtalo nuevamente."

    estado.value = "error"

  } finally {

    loading.value = false

  }

}
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