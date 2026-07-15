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
                    v-model="form.proyecto"
                    variant="outlined"
                />
            </v-col>

            <!-- CAMPO SELECCION DE ESTADOS -->
            <v-col cols="6">
                <v-select
                    label="Estado"
                    :items="estados"
                    item-title="nombre"
                    item-value="id"
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
                    item-value="usuario"
                    v-model="form.responsable"
                    variant="outlined"
                />
            </v-col>

            <!-- CAMPO FECHA INICIO -->
            <v-col cols="6">
                <v-text-field
                    label="Fecha inicio"
                    type="date"
                    v-model="form.fecha_creacion"
                    variant="outlined"
                />
            </v-col>

            <!-- CAMPO FECHA LIMITE -->
            <v-col cols="6">
                <v-text-field
                    label="Fecha límite"
                    type="date"
                    v-model="form.fecha_limite"
                    variant="outlined"
                />
            </v-col>

            <v-col cols="6">
                <v-text-field
                    label="Tiempo estimado (Horas)"
                    v-model="form.esfuerzo_estimado"
                    variant="outlined"
                    :rules="[rules.required]"
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
            >
                Guardar
            </v-btn>

        </div>

    </v-form>

</template>

<script setup>
import { ref, reactive, watch, computed, onMounted } from 'vue'
import { useProyectosStore } from '@/stores/proyectos'
import { useTareasStore } from '@/stores/tareas'
import assignmentService from '@/services/assignment.service'
import teamService from '@/services/team.service'


const props=defineProps({ task:Object })
const proyectosStore = useProyectosStore()
const proyectos = proyectosStore.proyectos
const store = useTareasStore()
const editMode = computed(() => !!props.task?.id)
const miembros = ref([])

const emit=defineEmits([
    'cancel',
    'save'
])

const estados=[
    {
    id:1,
    nombre:"Completado"
    },
    {
    id:2,
    nombre:"Por hacer"
    },
    {
    id:3,
    nombre:"En progreso"
    },
    {
    id:4,
    nombre:"En revision"
    }
]

const prioridades=[
    'Baja',
    'Media',
    'Alta'
]

const rules={required:v=>!!v||'Campo requerido'}

const cargarMiembros = async()=>{

    if(!form.proyecto){
        miembros.value=[]
        return
    }

    try{
        const res = await teamService.getByProject(form.proyecto)
        console.log(res.data)
        miembros.value=res.data
    } catch(error){
        console.error(error)
    }
}

const nuevoFormulario = () => ({
    titulo:'',
    descripcion:'',
    proyecto:null,
    estado:null,
    prioridad:'Media',
    responsable:null,
    fecha_limite:'',
    esfuerzo_estimado:null
})

const form=reactive(nuevoFormulario())
/* CARGAR DATOS AL EDITAR */
watch(
    ()=>props.task, (task)=>{

    if(task){

        Object.assign(form,{
            titulo:task.titulo,
            descripcion:task.descripcion,
            proyecto:task.proyecto,
            estado:task.estado,
            prioridad:task.prioridad,
            fecha_limite:task.fecha_limite,
            esfuerzo_estimado:task.esfuerzo_estimado,
            responsable:
            task.responsables?.[0]?.usuario_id ?? null
        })

    }else{
        Object.assign(form, nuevoFormulario())
    }
    },
    {
        immediate:true
    }
)

const guardar = async()=>{
    console.log(
        "DATOS ENVIADOS JSON:",
        JSON.stringify(form, null, 2)
    )

    emit('save', { ...form })
}

// FUNCION DE LIMPIEZA
const limpiar = () => {
  Object.assign(
    form,
    nuevoFormulario()
  )
}

watch(
()=>form.proyecto,
(valor)=>{

    if(valor){
        cargarMiembros()
    }

},
{
    immediate:true
}
)

</script>