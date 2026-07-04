<template>
  <v-container fluid>

    <!-- LOADING -->
    <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-4" />

    <!-- ERROR -->
    <v-alert v-if="error" type="error" class="mb-4">
      {{ error }}
    </v-alert>

    <!-- CONTENIDO -->
    <div v-if="project">

        <!-- HEADER -->
        <v-row class="mb-4" align="center">
          
          <v-col cols="12" md="8">
          <h2>{{ project.nombre }}</h2>
          </v-col>
        </v-row>

        <!-- INFO DEL PROYECTO -->
        <ProyectoInfoCard :project="project" />

        <!-- DETALLES DEL PROYECTO Y DEL EQUIPO -->
        <v-row>
          <!-- KPIS -->
          <v-col cols="12" md="6">
            <ProyectoKPIs :project-id="project.id" />  
          </v-col>

          <!-- CREACIÓN DEL EQUIPO (TEAM) Y ASIGNACIÓN DE ROLES -->
          <v-col cols="12" md="6">
            <EquipoProyecto :project-id="project.id" />   
            <DialogAsignarMiembro
              v-model="dialog"
              :project-id="projectId"
              @saved="cargarMiembros"
            />
          </v-col>
        </v-row>
        
        <!-- TAREAS -->
        <v-row> 
          <ProyectoUltimasTareas :project-id="project.id" />
        </v-row>

    </div>

  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'
import ProyectoInfoCard from '@/components/proyectos/ProyectoInfoCard.vue'
import ProyectoKPIs from '@/components/proyectos/ProyectoKPIs.vue'
import EquipoProyecto from '@/components/proyectos/EquipoProyecto.vue'
import ProyectoUltimasTareas from '@/components/proyectos/ProyectoUltimasTareas.vue'

const route = useRoute()

console.log(route.params)
console.log(route.params.id)

const projectId = route.params.id
api.get(`/api/projects/${projectId}/`)

const project = ref(null)
const loading = ref(false)
const error = ref(null)

const fetchProject = async () => {
  loading.value = true
  error.value = null

  try {
    const res = await api.get(`/api/projects/${route.params.id}/`)
    project.value = res.data
  } catch (err) {
    error.value =
      err.response?.data?.message ||
      'Error al cargar el proyecto'
  } finally {
    loading.value = false
  }
}

const estadoColor = (estado) => {
  switch (estado) {
    case 'En progreso':
      return 'warning'
    case 'Completado':
      return 'success'
    case 'Pausado':
      return 'error'
    case 'Planificacion':
      return 'info'
    default:
      return 'grey'
  }
}

onMounted(() => {
  fetchProject()
})
</script>