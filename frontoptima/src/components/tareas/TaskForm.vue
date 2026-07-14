<template>

    <v-form @submit.prevent="guardar">

        <v-row>
            <!-- CAMPO TITULO -->
            <v-col cols="12">
                <v-text-field
                    label="Título"
                    v-model="form.titulo"
                    variant="outlined"
                    :rules="[rules.required]"
                />
            </v-col>

            <!-- CAMPO DESCRIPCIÓN -->
            <v-col cols="12">
                <v-textarea
                    label="Descripción"
                    rows="3"
                    v-model="form.descripcion"
                    variant="outlined"
                />
            </v-col>

            <!-- CAMPO SELECION DE PROYECTO -->
            <v-col cols="6">
                <v-select
                    label="Proyecto"
                    :item-title="'nombre'"
                    :item-value="'id'"
                    :items="proyectos"
                    v-model="form.proyectoId"
                    variant="outlined"
                />
            </v-col>

            <!-- CAMPO SELECCION DE ESTADOS -->
            <v-col cols="6">
                <v-select
                    label="Estado"
                    :items="estados"
                    v-model="form.estado"
                    variant="outlined"
                    placeholder="Seleccionar estado de la tarea"
                    persistent-placeholder
                />
            </v-col>

            <!-- CAMPO PRIORIDAD -->
            <v-col cols="6">
                <v-select
                    label="Prioridad"
                    :items="prioridades"
                    v-model="form.prioridad"
                    variant="outlined"
                    placeholder="Seleccionar prioridad"
                    persistent-placeholder
                />
            </v-col>

            <!-- CAMPO RESPONSABLE-->
            <v-col cols="6">
                <v-select
                    label="Responsable"
                    :items="miembros"
                    item-title="nombre_usuario"
                    item-value="id"
                    v-model="form.responsable"
                    variant="outlined"
                    placeholder="Seleccionar responsable"
                    persistent-placeholder
                />
            </v-col>

            <!-- CAMPO FECHA INICIO -->
            <v-col cols="6">
                <v-text-field
                    label="Fecha inicio"
                    type="date"
                    v-model="form.fechaInicio"
                    variant="outlined"
                />
            </v-col>

            <!-- CAMPO FECHA LIMITE -->
            <v-col cols="6">
                <v-text-field
                    label="Fecha límite"
                    type="date"
                    v-model="form.fechaLimite"
                    variant="outlined"
                />
            </v-col>
        </v-row>

        <v-divider class="my-4"/>

        <div class="d-flex justify-end">

            <!-- BTON GUARDAR -->
            <v-btn
                type="submit"
                color="accent"
                class="mr-2"
                @click="$emit('cancel')"
            >
                Guardar
            </v-btn>

        </div>

    </v-form>

</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue'
import { useProyectosStore } from '@/stores/proyectos'
import { useTareasStore } from '@/stores/tareas'
import Swal from 'sweetalert2'

const proyectosStore = useProyectosStore()
const proyectos = proyectosStore.proyectos
const store = useTareasStore()


const props=defineProps({
    task:Object
})

const cargarMiembros = async () => {
  if (!form.proyectoId) {
    miembros.value = []
    return
  }

  loading.value = true

  try {

    const res = await teamService.getByProject(form.proyectoId)
    miembros.value = res.data

  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}
const emit=defineEmits([
    'cancel',
    'save'
])

const estados=[
    'Por hacer',
    'En progreso',
    'En revision',
    'Finalizada'
]

const prioridades=[
    'Baja',
    'Media',
    'Alta'
]

const rules={
    required:v=>!!v||'Campo requerido'
}

const nuevoFormulario=()=>({
    titulo:'',
    descripcion:'',
    proyectoId:null,
    estado:ref(null),
    prioridad:ref(null),
    responsable:'',
    fechaInicio:'',
    fechaLimite:'',
    etiquetas:[]
})

const form=reactive(nuevoFormulario())

watch(()=>props.task,(value)=>{

    Object.assign(form,nuevoFormulario(),value||{})

},{immediate:true})

const guardar = async () => {

    if (editMode.value) {
    await store.actualizarTarea(editId.value, form)
  } else {
    await store.crearTarea(form)
  }

  limpiar()
}

// FUNCION DE LIMPIEZA
const limpiar = () => {
  form.titulo = ''
  form.descripcion = ''
  form.proyectoId = ref(null),
  form.estado = ref(null),
  form.prioridad = ref(null),
  form.responsable = '',
  form.fechaInicio = ''
  form.fechaLimite = ''
  form.etiquetas = []

}

onMounted(async () => {
  await store.obtenerTareas()
})
</script>