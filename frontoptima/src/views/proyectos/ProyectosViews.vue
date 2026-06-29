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
        <v-btn color="primary" @click="dialog = true">
          Nuevo proyecto
        </v-btn>
      </v-col>
    </v-row>

    <!-- LISTA -->
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

          <v-chip
            :color="estadoColor(p.estado)"
            class="mt-2"
            size="small"
          >
            {{ p.estado }}
          </v-chip>

          <v-divider class="my-3" />

          <div class="d-flex justify-space-between">

            <v-btn
              size="small"
              color="primary"
              @click="editar(p)"
            >
              Editar
            </v-btn>

            <v-btn
              size="small"
              color="red"
              @click="store.eliminarProyecto(p.id)"
            >
              Eliminar
            </v-btn>

          </div>

        </v-card>
      </v-col>
    </v-row>

    <!-- DIALOG -->
    <v-dialog v-model="dialog" max-width="500">
      <v-card class="pa-4">

        <h3 class="mb-4">
          {{ editMode ? 'Editar proyecto' : 'Nuevo proyecto' }}
        </h3>

        <v-text-field
          v-model="form.nombre"
          label="Nombre"
          variant="outlined"
        />

        <v-text-field
          v-model="form.descripcion"
          label="Descripción"
          variant="outlined"
          class="mt-3"
        />

        <v-select
          v-model="form.estado"
          :items="['activo', 'pausado', 'terminado']"
          label="Estado"
          class="mt-3"
          variant="outlined"
        />

        <v-btn
          color="primary"
          block
          class="mt-4"
          @click="guardar"
        >
          Guardar
        </v-btn>

      </v-card>
    </v-dialog>

  </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { useProyectosStore } from '@/stores/proyectos'

const store = useProyectosStore()

const search = ref('')
const dialog = ref(false)
const editMode = ref(false)
const editId = ref(null)

const form = reactive({
  nombre: '',
  descripcion: '',
  estado: 'activo',
})

const proyectosFiltrados = computed(() => {
  return store.proyectos.filter(p =>
    p.nombre.toLowerCase().includes(search.value.toLowerCase())
  )
})

const guardar = () => {
  if (editMode.value) {
    store.actualizarProyecto(editId.value, form)
  } else {
    store.agregarProyecto(form)
  }

  limpiar()
}

const editar = (p) => {
  editMode.value = true
  editId.value = p.id

  form.nombre = p.nombre
  form.descripcion = p.descripcion
  form.estado = p.estado

  dialog.value = true
}

const limpiar = () => {
  form.nombre = ''
  form.descripcion = ''
  form.estado = 'activo'

  editMode.value = false
  editId.value = null
  dialog.value = false
}

const estadoColor = (estado) => {
  switch (estado) {
    case 'activo': return 'green'
    case 'pausado': return 'orange'
    case 'terminado': return 'blue'
    default: return 'grey'
  }
}
</script>