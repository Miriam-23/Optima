<template>
  <div>

    <h2 class="mb-6">Proyectos</h2>

    <!-- ACCIONES -->
    <v-row class="mb-4">
      <v-col cols="12" md="8">
        <v-text-field
          v-model="search"
          label="Buscar proyecto"
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
        />
      </v-col>

      <v-col cols="12" md="4" class="text-right">
        <v-btn color="secondary" @click="dialog = true">
          Nuevo proyecto
        </v-btn>
      </v-col>
    </v-row>

    <!-- LISTA -->
    <v-progress-linear indeterminate color="primary" v-if="store.loading"/>

    <v-row>
      <v-col
        cols="12"
        md="4"
        v-for="p in proyectosFiltrados"
        :key="p.id"
      >
        <v-card class="pa-4" elevation="2">

          <h3>{{ p.nombre }}</h3>
          <p class="text-medium-emphasis">{{ p.descripcion }}</p>

          <v-chip :color="estadoColor(p.estado_general)">
            {{ p.estado_general }}
          </v-chip>

          <v-divider class="my-3" />

          <div class="d-flex align-center ga-2">
            <!-- VER DETALLES -->
            <v-btn 
              size="small"
              color="accent"
              @click="abrirProyecto(p.id)">
              <v-icon>mdi-eye-outline</v-icon>
            </v-btn>

            <template v-if="esProjectManager(p.id)">
              <!-- EDITAR -->
              <v-btn
                size="small"
                color="warning"
                @click="editar(p)"
              >
                <v-icon>mdi-pencil-outline</v-icon>
              </v-btn>

              <!-- ELIMINAR -->
              <v-btn
                size="small"
                color="red"
                 @click="confirmarEliminar(p.id)"
              >
                <v-icon>mdi-delete-outline</v-icon>
              </v-btn>

            </template>

          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- DIALOG -->
    <v-dialog v-model="dialog" max-width="500">
      <v-card class="pa-4" style="overflow: visible;">

        <h3 class="mb-4">
          {{ editMode ? 'Editar proyecto' : 'Nuevo proyecto' }}
        </h3>

        <!-- Errores para la UI -->
        <v-alert
          v-if="errorGuardado"
          type="error"
          variant="tonal"
          border="start"
          icon="mdi-alert-circle-outline"
          closable
          class="mb-4"
          @click:close="errorGuardado = null"
        >
          <div style="white-space: normal; word-break: break-word; line-height: 1.4;">
            {{ errorGuardado }}
          </div>
        </v-alert>

        <v-text-field
          v-model="form.nombre"
          label="Nombre"
        />

        <v-textarea
          v-model="form.descripcion"
          label="Descripción"
        />

        <v-text-field
          v-model="form.fecha_inicio"
          type="date"
          label="Fecha inicio"
        />

        <v-text-field
          v-model="form.fecha_fin"
          type="date"
          label="Fecha fin"
        />

        <v-select
          v-model="form.estado_general"
          :items="[
            'Planificacion',
            'En progreso',
            'Completado',
            'Pausado'
          ]"
          label="Estado"
        />

        <v-btn
          color="accent"
          block
          class="mt-4"
          :loading="guardando"
          :disabled="guardando"
          @click="guardar"
        >
          Guardar
        </v-btn>

      </v-card>
    </v-dialog>

  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { computed, reactive, ref } from 'vue'
import { useProyectosStore } from '@/stores/proyectos'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import teamService from '@/services/team.service'
import Swal from 'sweetalert2'

const authStore = useAuthStore()
const router = useRouter()

// VERIFICACION DE SI ES PROYECT MANAGER PARA EDITAR Y ELIMINAR UN PROYECTO
// POR ELLO VEMOS LOS MIEMBROS DEL EQUIPO PARA HACER UNA COMPARACIÓN 
const miembros = ref([])

const cargarMiembros = async () => {
  const res = await teamService.getAll()
  miembros.value = res.data
}

// VERIFICAMOS
const esProjectManager = (projectId) => {
  const miRegistro = miembros.value.find(
    m =>
      m.proyecto === projectId &&
      m.usuario === authStore.user?.id
  )

  return miRegistro?.nombre_rol === 'Project Manager'
}


const store = useProyectosStore()
const search = ref('')
const dialog = ref(false)
const editMode = ref(false)
const editId = ref(null)

// FUNCION ABRIR PROYECTO PARA VER SUS DETALLES
const abrirProyecto = (id) => {
  router.push(`/proyectos/${id}`)
}

// FORMULARIO PARA LA CREACION DE UN PROYECTO
const form = reactive({
  nombre: '',
  descripcion: '',
  fecha_inicio: '',
  fecha_fin: '',
  estado_general: 'Planificacion'
})

// FILTRACION POR PROYECTOS
const proyectosFiltrados = computed(() => {
  return store.proyectos.filter(p =>
    p.nombre.toLowerCase().includes(search.value.toLowerCase())
  )
})

// FUNCION GUARDAR PROYECTO
const guardando = ref(false)
const errorGuardado = ref(null)

const guardar = async () => {
  if (form.fecha_inicio && form.fecha_fin && form.fecha_fin < form.fecha_inicio) {
    errorGuardado.value = 'La fecha de fin no puede ser anterior a la fecha de inicio.'
    return
  }

  guardando.value = true
  errorGuardado.value = null

  try {
    if (editMode.value) {
      await store.actualizarProyecto(editId.value, form)
    } else {
      await store.crearProyecto(form)
    }
    limpiar()
  } catch (err) {
    errorGuardado.value = err.response?.data?.fecha_fin?.[0]
      || err.response?.data?.detail
      || Object.values(err.response?.data || {}).flat().join(' ')
      || 'No se pudo guardar el proyecto.'
  } finally {
    guardando.value = false
  }
}

// FUNCION EDITAR PROYECTO
const editar = (p) => {
  editMode.value = true
  editId.value = p.id

  form.nombre = p.nombre
  form.descripcion = p.descripcion
  form.estado_general = p.estado_general
  form.fecha_inicio = p.fecha_inicio
  form.fecha_fin = p.fecha_fin

  dialog.value = true
}

const confirmarEliminar = async (id) => {

  const result = await Swal.fire({
    title: '¿Deseas eliminar este proyecto?',
    text: 'Esta acción no se puede deshacer.',
    icon: 'warning',
    background: 'rgba(13, 194, 211,0.6)',
    color: '#fff',
    backdrop: 'rgba(0,0,0,0.4)',
    showCancelButton: true,
    confirmButtonText: 'Eliminar',
    cancelButtonText: 'Cancelar',
    confirmButtonColor: 'success',
    cancelButtonColor: 'error',
    confirmButtonColor: '#d32f2f', // Rojo
    cancelButtonColor: '#1976D2',
    customClass: {
      popup: 'swal2-glass'
    }
  })

  if (!result.isConfirmed) return

  try {

    await store.eliminarProyecto(id)

    Swal.fire({
      title: 'Proyecto eliminado',
      text: 'El proyecto se elimino correctamente.',
      icon: 'success',
      background: 'rgba(0,0,0,0.6)',
      color: '#fff',
      backdrop: 'rgba(0,0,0,0.4)',
      showConfirmButton: false,
      timer: 1500,
      timerProgressBar: false,
      customClass: {
        popup: 'swal2-glass'
      }
    })

  } catch (error) {

    Swal.fire({
      title: 'Error',
      text: 'No se pudo eliminar el proyecto.',
      icon: 'error',
      background: 'rgba(0,0,0,0.6)',
      color: '#fff',
      backdrop: 'rgba(0,0,0,0.4)',
      showConfirmButton: false,
      timer: 1500,
      timerProgressBar: false,
      customClass: {
        popup: 'swal2-glass'
      }
    })

    console.error(error)
  }
}

// FUNCION DE LIMPIEZA
const limpiar = () => {
  form.nombre = ''
  form.descripcion = ''
  form.fecha_inicio = ''
  form.fecha_fin = ''
  form.estado_general = 'Planificacion'

  editMode.value = false
  editId.value = null
  dialog.value = false
  errorGuardado.value = null 
}

// FUNCION DE ESTADO POR COLOR
const estadoColor = (estado) => {
  switch (estado) {
    case 'Planificacion': return 'blue'
    case 'En progreso': return 'green'
    case 'Pausado': return 'orange'
    case 'Completado': return 'grey'
    default: return 'grey'
  }
}

// onMounted(() => {
//   store.obtenerProyectos()
// })

// PRUEBA
onMounted(async () => {
  await store.obtenerProyectos()
  await cargarMiembros()
})
</script>