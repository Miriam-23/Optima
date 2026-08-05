<template>
  <v-container fluid class="login-wrapper pa-0">
    <v-row no-gutters class="fill-height">

      <!-- Panel izquierdo -->
      <v-col
        cols="12"
        md="6"
        class="left-panel d-flex justify-center align-center"
      >
        <v-img
          :src="logoLight"
          width="520"
        />
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
          class="login-card pa-8 text-center text-white"
          :style="{
            backgroundColor:'rgba(0,0,0,.5)',
            backdropFilter:'blur(10px)'
          }"
        >

          <!-- FORMULARIO -->
          <div v-if="estado === 'form'">

            <v-icon
              size="80"
              color="primary"
              class="mb-5"
            >
              mdi-lock-reset
            </v-icon>

            <h2 class="mb-3">
              Restablecer contraseña
            </h2>

            <p class="mb-6">
              Escribe una nueva contraseña para tu cuenta.
            </p>

            <v-form
              ref="form"
              @submit.prevent="restablecerPassword"
            >

                <v-text-field
                    v-model="password"
                    label="Nueva contraseña"
                    prepend-inner-icon="mdi-lock"
                    :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                    :type="showPassword ? 'text' : 'password'"
                    variant="outlined"
                    :rules="passwordRules"
                    @click:append-inner="showPassword = !showPassword"
                />

                <v-progress-linear
                    :model-value="passwordStrength.value"
                    :color="passwordStrength.color"
                    height="8"
                    rounded
                    class="mb-2"
                />

                <div
                    class="text-caption mb-4"
                    :class="`text-${passwordStrength.color}`"
                >
                    Fortaleza:
                    {{ passwordStrength.text }}
                </div>

                <v-text-field
                    v-model="confirmPassword"
                    label="Confirmar contraseña"
                    prepend-inner-icon="mdi-lock-check"
                    :append-inner-icon="showConfirm ? 'mdi-eye-off' : 'mdi-eye'"
                    :type="showConfirm ? 'text' : 'password'"
                    variant="outlined"
                    :rules="confirmRules"
                    @click:append-inner="showConfirm = !showConfirm"
                />

                <v-btn
                    block
                    color="primary"
                    :loading="loading"
                    type="submit"
                >
                    Restablecer contraseña
                </v-btn>

            </v-form>

          </div>

          <!-- ÉXITO -->
          <div v-else-if="estado === 'success'">

            <v-icon
              color="success"
              size="80"
              class="mb-5"
            >
              mdi-check-circle
            </v-icon>

            <h2 class="mb-3">
              ¡Contraseña actualizada!
            </h2>

            <p class="mb-6">
              {{ mensaje }}
            </p>

            <RouterLink to="/login">

              <v-btn
                color="primary"
                block
              >
                Iniciar sesión
              </v-btn>

            </RouterLink>

          </div>

          <!-- ERROR -->
          <div v-else>

            <v-icon
              color="error"
              size="80"
              class="mb-5"
            >
              mdi-alert-circle
            </v-icon>

            <h2 class="mb-3">
              Enlace inválido
            </h2>

            <p class="mb-6">
              {{ mensaje }}
            </p>

            <RouterLink to="/forgot-password">

              <v-btn
                color="primary"
                block
              >
                Solicitar otro enlace
              </v-btn>

            </RouterLink>

          </div>

        </v-card>

      </v-col>

    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed } from "vue"
import { useRoute } from "vue-router"
import authService from "@/services/auth.service"
import logoLight from "@/assets/images/logo_ligth.png"

const form = ref(null)

const route = useRoute()
const estado = ref("form")
const mensaje = ref("")
const uid = route.query.uid
const token = route.query.token
const password = ref("")
const confirmPassword = ref("")

const loading = ref(false)

const showPassword = ref(false)
const showConfirm = ref(false)

if (!uid || !token) {

    estado.value = "error"

    mensaje.value =
        "El enlace de recuperación es inválido o está incompleto."

}


const passwordRules = [
    v => !!v || "La contraseña es obligatoria.",
    v => v.length >= 8 || "Debe tener al menos 8 caracteres.",
    v => /[A-Z]/.test(v) || "Debe contener una mayúscula.",
    v => /\d/.test(v) || "Debe contener un número."
]

const confirmRules = computed(() => [
    v => !!v || "Confirma la contraseña.",
    v => v === password.value || "Las contraseñas no coinciden."
])

const restablecerPassword = async () => {

    if (estado.value === "error") return

    const { valid } = await form.value.validate()

    if (!valid) return

    loading.value = true

    try {

        const response = await authService.resetPassword({
            uid,
            token,
            new_password: password.value
        })

        mensaje.value = response.data.mensaje

        estado.value = "success"

    } catch (error) {

        estado.value = "error"

        mensaje.value =
            error.response?.data?.mensaje ||
            error.response?.data?.error ||
            "El enlace es inválido o ha expirado."

    } finally {

        loading.value = false

    }

}

const passwordStrength = computed(() => {

    const value = password.value

    if (!value)
        return {
            text: "",
            color: "",
            value: 0
        }

    let score = 0

    if (value.length >= 8) score++
    if (/[A-Z]/.test(value)) score++
    if (/[a-z]/.test(value)) score++
    if (/\d/.test(value)) score++
    if (/[^A-Za-z0-9]/.test(value)) score++

    if (score <= 2)
        return {
            text: "Débil",
            color: "error",
            value: 35
        }

    if (score <= 4)
        return {
            text: "Media",
            color: "warning",
            value: 70
        }

    return {
        text: "Fuerte",
        color: "success",
        value: 100
    }

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