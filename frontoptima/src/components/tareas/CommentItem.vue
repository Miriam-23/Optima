<!-- <template>

  <v-card class="pa-3 mb-3" variant="outlined">

    <div class="d-flex">

      <v-avatar color="primary">
        <v-icon>mdi-account</v-icon>
      </v-avatar>


      <div class="ml-3">

        <strong>{{ comentario.nombre_autor }}</strong>

        <p class="mb-1">{{ comentario.contenido }}</p>


        <small>{{ fecha }}</small>


      </div>


      <v-spacer/>


      <v-btn
        v-if="puedeEliminar"
        icon="mdi-delete"
        size="small"
        color="error"
        @click="$emit('delete', comentario.id)"
      />

    </div>

  </v-card>
</template> -->
<template>
  <v-card
    class="comment-card pa-3 mb-3"
    elevation="0"
    rounded="lg"
  >

    <div class="d-flex align-start">

      <!-- Avatar -->
      <v-avatar
        size="42"
        color="primary"
        class="mr-3"
      >
        <span class="text-white font-weight-bold">
          {{ inicial }}
        </span>
      </v-avatar>


      <!-- Contenido -->
      <div class="flex-grow-1">

        <div class="d-flex align-center">

          <strong class="text-body-1">
            {{ comentario.nombre_autor }}
          </strong>

          <span class="text-caption text-medium-emphasis ml-3">
            {{ fecha }}
          </span>

        </div>


        <div class="comment-text mt-2">
          {{ comentario.contenido }}
        </div>

      </div>


      <!-- Acciones -->
      <v-btn
      v-if="puedeEliminar"
        icon="mdi-delete-outline"
        size="small"
        variant="text"
        color="error"
        class="delete-btn"
        @click="$emit('delete', comentario.id)"
      />

    </div>

  </v-card>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  comentario:{
    type:Object,
    required:true
  }
})

const authStore = useAuthStore()

const puedeEliminar = computed(() => {
  const usuarioActual = authStore.user

  if (!usuarioActual) return false

  // Autor
  if (props.comentario.usuario === usuarioActual.id)
    return true

  // Project Manager
  return props.comentario.puede_gestionar === true
})


//const fecha = new Date(props.comentario.fecha_creacion).toLocaleString('es-MX')
const fecha = computed(() => {

  return new Date(
    props.comentario.fecha_creacion
  ).toLocaleString('es-MX',{
    dateStyle:'medium',
    timeStyle:'short'
  })

})

defineEmits([
 'delete'
])

const inicial = computed(() => {

  return props.comentario.nombre_autor
    ?.charAt(0)
    .toUpperCase() || '?'

})
</script>

<style scoped>
.comment-card{
  background: rgb(var(--v-theme-surface));
  border:1px solid rgba(0,0,0,.08);
  transition:.25s ease;
}

.comment-card:hover{
  border-color:rgb(var(--v-theme-primary));
  transform:translateY(-2px);
  box-shadow:0 6px 18px rgba(0,0,0,.08);
}

.comment-text{
  background:rgba(var(--v-theme-primary), .06);
  padding:10px 14px;
  border-radius:12px;
  color:rgb(var(--v-theme-on-surface));
  line-height:1.5;
  white-space:pre-line;
}

.delete-btn{
  opacity:.5;
  transition:.2s;
}

.comment-card:hover .delete-btn{
  opacity:1;
}

</style>