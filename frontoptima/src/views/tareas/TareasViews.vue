<template>
  <div>

    <h2 class="mb-4">Tareas</h2>

    <!-- SELECT PROYECTO -->
    <v-select
      v-model="proyectoSeleccionado"
      :items="proyectos"
      item-title="nombre"
      item-value="id"
      label="Seleccionar proyecto"
      variant="outlined"
      class="mb-4"
    />

    <v-btn color="primary" class="mb-4" @click="dialog = true">
      Nueva tarea
    </v-btn>

    <!-- KANBAN -->
    <v-row>

      <!-- TODO -->
      <v-col cols="12" md="4">
        <v-card class="pa-4">
          <h3>Por hacer</h3>

          <v-card
            v-for="t in tareasFiltradas.todo"
            :key="t.id"
            class="pa-3 mt-3"
          >
            <strong>{{ t.titulo }}</strong>
            <p>{{ t.descripcion }}</p>

            <v-btn size="x-small"
              @click="store.cambiarEstado(t.id, 'En progreso')"
            >
              Empezar
            </v-btn>
          </v-card>

        </v-card>
      </v-col>

      <!-- DOING -->
      <v-col cols="12" md="4">
        <v-card class="pa-4">
          <h3>En progreso</h3>

          <v-card
            v-for="t in tareasFiltradas.doing"
            :key="t.id"
            class="pa-3 mt-3"
          >
            <strong>{{ t.titulo }}</strong>

            <v-btn size="x-small" color="green"
              @click="store.cambiarEstado(t.id, 'Finalizada')"
            >
              Terminar
            </v-btn>
          </v-card>

        </v-card>
      </v-col>

      <!-- DONE -->
      <v-col cols="12" md="4">
        <v-card class="pa-4">
          <h3>Terminadas</h3>

          <v-card
            v-for="t in tareasFiltradas.done"
            :key="t.id"
            class="pa-3 mt-3"
          >
            <strong>{{ t.titulo }}</strong>

            <v-btn size="x-small" color="red">
              Eliminar
            </v-btn>
          </v-card>

        </v-card>
      </v-col>

    </v-row>

    <!-- DIALOG -->
    <v-dialog v-model="dialog" max-width="500">
      <v-card class="pa-4">

        <h3>Nueva tarea</h3>

        <v-text-field v-model="form.titulo" label="Título" />
        <v-text-field v-model="form.descripcion" label="Descripción" />

        <v-select
          v-model="form.prioridad"
          :items="['Baja','Media','Alta']"
          label="Prioridad"
        />

        <v-btn color="primary" block @click="guardar">
          Guardar
        </v-btn>

      </v-card>
    </v-dialog>

  </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { useTareasStore } from '@/stores/tareas'
import { useProyectosStore } from '@/stores/proyectos'

const store = useTareasStore()
const proyectosStore = useProyectosStore()

const dialog = ref(false)

const proyectoSeleccionado = ref(1)

const proyectos = computed(() => proyectosStore.proyectos)

/* FILTRADO POR PROYECTO */
const tareasFiltradas = computed(() => {
  const tareas = store.porProyecto(proyectoSeleccionado.value)

  return {
    todo: tareas.filter(t => t.estado === 'Por hacer'),
    doing: tareas.filter(t => t.estado === 'En progreso'),
    done: tareas.filter(t => t.estado === 'Finalizada'),
  }
})

const form = reactive({
  titulo: '',
  descripcion: '',
  prioridad: 'Media',
})

const guardar = () => {
  store.agregarTarea({
    ...form,
    estado: 'Por hacer',
    proyectoId: proyectoSeleccionado.value,
  })

  dialog.value = false
}
</script>