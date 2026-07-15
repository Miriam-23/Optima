<template>

<v-card
  class="pa-3 mb-3"
  variant="outlined"
>

<div class="d-flex">

<v-avatar
  color="primary"
>

<v-icon>
mdi-account
</v-icon>

</v-avatar>


<div class="ml-3">

<strong>
{{ comentario.nombre_autor }}
</strong>


<p class="mb-1">
{{ comentario.contenido }}
</p>


<small>
{{ fecha }}
</small>


</div>


<v-spacer/>


<v-btn
 icon="mdi-delete"
 size="small"
 color="error"
 @click="$emit('delete', comentario.id)"
/>


</div>

</v-card>

</template>


<script setup>

const props = defineProps({

 comentario:{
  type:Object,
  required:true
 }

})


const fecha = new Date(
 props.comentario.fecha_creacion
).toLocaleString('es-MX')


defineEmits([
 'delete'
])

</script>