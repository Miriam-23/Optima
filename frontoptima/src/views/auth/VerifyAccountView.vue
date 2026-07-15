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
            Estamos validando tu enlace de verificación.
            Esto solo tomará unos segundos.
          </p>

        </v-card>

      </v-col>

    </v-row>
  </v-container>
</template>

<script setup>
import logoLight from '@/assets/images/logo_ligth.png'
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