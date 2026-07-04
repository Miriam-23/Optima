<template>
  <v-card class="pa-4 mb-4" elevation="2">

    <!-- HEADER -->
    <div class="d-flex justify-space-between align-center mb-3">

      <h3>Equipo del proyecto</h3>

      <!-- SOLO PUEDE AGREGAR MIEMBROS AL EQUIPO EL PROJECT MANAGER -->
      <v-btn
        v-if="esProjectManager"
        color="primary"
        size="small"
        @click="dialog = true"
      >
        + Agregar miembro
      </v-btn>

    </div>

    <!-- LOADING -->
    <v-progress-linear
      v-if="loading"
      indeterminate
      color="primary"
      class="mb-3"
    />

    <!-- LISTA -->
    <v-list v-if="miembros.length">

      <v-list-item
        v-for="m in miembros"
        :key="m.id"
      >

        <template #prepend>
          <v-icon color="primary">
            mdi-account
          </v-icon>
        </template>

        <v-list-item-title>
          {{ m.nombre_usuario }}
        </v-list-item-title>

        <v-list-item-subtitle>
          {{ m.email_usuario }} - {{ m.nombre_rol }}
        </v-list-item-subtitle>

        <template #append>

          <v-chip size="small" color="primary" class="mr-2">
            {{ m.nombre_rol }}
          </v-chip>

          <!-- SOLO PUEDE ELIMINAR MIENBROS EL PROJECT MANAGER-->
          <v-btn
            v-if="esProjectManager"
            icon
            size="small"
            color="red"
            @click="eliminar(m.id)"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>

        </template>

      </v-list-item>

    </v-list>

    <!-- EMPTY -->
    <v-alert
      v-else-if="!loading"
      type="info"
      class="mt-3"
    >
      No hay miembros asignados
    </v-alert>

    <!-- DIALOG -->
    <DialogAsignarMiembro
      v-model="dialog"
      :project-id="projectId"
      @saved="cargarMiembros"
    />

  </v-card>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import teamService from '@/services/team.service'
import DialogAsignarMiembro from './DialogAsignarMiembro.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const props = defineProps({
  projectId: {
    type: Number,
    required: true
  }
})

const miembros = ref([])
const loading = ref(false)
const dialog = ref(false)

const cargarMiembros = async () => {

  loading.value = true

  try {

    const res = await teamService.getAll()

    // filtramos por proyecto
    miembros.value = res.data.filter(
      m => m.proyecto === props.projectId
    )

  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const eliminar = async (id) => {

  try {

    await teamService.remove(id)

    miembros.value = miembros.value.filter(m => m.id !== id)

  } catch (err) {
    console.error('Error al eliminar miembro', err)
  }
}

const esProjectManager = computed(() => {
  const miRegistro = miembros.value.find(
    m => m.usuario === authStore.user.id
  )

  return miRegistro?.nombre_rol === 'Project Manager'
})

onMounted(() => {
  cargarMiembros()
})


</script>