<template>
  <v-layout class="d-flex justify-center align-center" :style="{ backgroundImage: `url(${logo_optima})`,
      backgroundSize: 'cover', backgroundPosition: 'center', height: '100vh' }">
    <router-view />
  </v-layout>
</template>

<script lang="js" setup>
import logo_optima from '../assets/logo_optima.png'
</script>