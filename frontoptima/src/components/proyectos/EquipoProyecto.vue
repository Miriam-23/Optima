<template>
  <v-card class="pa-4 mb-4" elevation="2">

    <!-- HEADER -->
    <div class="d-flex justify-space-between align-center mb-3">
      <h3>Equipo del proyecto</h3>

      <!-- SOLO PUEDE AGREGAR MIEMBROS EL PROJECT MANAGER -->
      <v-btn
        v-if="esProjectManager"
        color="primary"
        size="small"
        @click="dialog = true"
      >
        + Agregar miembro
      </v-btn>
    </div>

    <!-- LISTA (Ya no hay loading porque el padre maneja la carga global) -->
    <v-list v-if="miembros.length">
      <v-list-item v-for="m in miembros" :key="m.id">

        <template #prepend>
          <v-icon color="primary">mdi-account</v-icon>
        </template>

        <v-list-item-title class="font-weight-bold">
          {{ m.nombre }}
        </v-list-item-title>

        <v-list-item-subtitle>
          {{ m.email }}
        </v-list-item-subtitle>

        <template #append>
          <v-chip size="small" color="primary" variant="tonal" class="mr-2">
            {{ m.rol }}
          </v-chip>

          <!-- SOLO PUEDE ELIMINAR MIEMBROS EL PROJECT MANAGER, Y NO PUEDE ELIMINARSE A SÍ MISMO -->
          <v-btn
            v-if="esProjectManager && m.usuario_id !== authStore.user.id"
            icon
            size="small"
            color="error"
            variant="text"
            @click="eliminar(m.id_asignacion)" 
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>

      </v-list-item>
    </v-list>

    <!-- EMPTY STATE -->
    <v-alert v-else type="info" class="mt-3" variant="tonal">
      No hay miembros asignados a este proyecto.
    </v-alert>

    <!-- DIALOG (Encapsulado correctamente) -->
        <DialogAsignarMiembro
          v-model="dialog"
          :project-id="Number(projectId)"
          @saved="onMiembroModificado"
        />

  </v-card>
</template>

<script setup>
import { computed, ref } from 'vue'
import teamService from '@/services/team.service'
import DialogAsignarMiembro from './DialogAsignarMiembro.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// 1. Recibimos la data ya masticada desde Django
const props = defineProps({
  projectId: {
    type: [Number, String],
    required: true
  },
  equipoData: {
    type: Array,
    default: () => []
  }
})

// Declaramos eventos para avisarle al componente padre que algo cambió
const emit = defineEmits(['refresh'])

const dialog = ref(false)

// 2. Mapeamos la data del prop a la variable reactiva
const miembros = computed(() => props.equipoData || [])

// 3. Validación RBAC intacta pero usando la nueva data
const esProjectManager = computed(() => {
  if (!authStore.user) return false
  const miRegistro = miembros.value.find(
    m => m.usuario_id === authStore.user.id
  )
  return miRegistro?.rol === 'Project Manager'
})

// 4. Eliminación de miembros
const eliminar = async (id) => {
  // Aquí podrías agregar un confirm() de JS rápido para evitar clics accidentales
  if(!confirm('¿Estás seguro de quitar a este miembro del proyecto?')) return

  try {
    // Le pegamos al endpoint DELETE que armó Miri
    await teamService.remove(id)
    
    // Disparamos el evento para que el Dashboard maestro (padre) recargue TODA la info
    onMiembroModificado()
  } catch (err) {
    console.error('Error al eliminar miembro', err)
  }
}

// 5. Centralizamos la recarga
const onMiembroModificado = () => {
  dialog.value = false
  emit('refresh') // Le grita al padre: "¡Oye, alguien fue agregado/eliminado, vuelve a llamar a la API!"
}
</script>