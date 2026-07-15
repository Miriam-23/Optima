<template>
    <div>
        <h3 class="mb-4">Comentarios</h3>

        <!-- NUEVO COMENTARIO -->
        <v-card variant="outlined" class="pa-3 mb-5">
            <v-textarea
                v-model="nuevoComentario"
                label="Escribe un comentario..."
                rows="3"
                auto-grow
                hide-details
            />

            <div class="d-flex justify-end mt-3">
                <v-btn
                    color="primary"
                    :loading="loading"
                    :disabled="!nuevoComentario.trim()"
                    @click="agregarComentario"
                >
                    <v-icon start>mdi-send</v-icon>
                    Comentar
                </v-btn>
            </div>
        </v-card>

        <!-- LISTA DE COMENTARIOS -->
        <v-card v-if="comentarios.length" variant="tonal">
            <!-- <v-list>
                <v-list-item
                    v-for="comentario in comentarios"
                    :key="comentario.id"
                >
                    <template #prepend>
                        <v-avatar
                            color="primary"
                        >
                            <v-icon> mdi-account</v-icon>
                        </v-avatar>
                    </template>

                    <v-list-item-title>
                        {{ comentario.nombre_autor }}
                    </v-list-item-title>

                    <v-list-item-subtitle>
                        {{ comentario.contenido }}
                        <br>
                        <small>
                            {{ formatDate(comentario.fecha_creacion) }}
                        </small>
                    </v-list-item-subtitle>

                    <template #append>
                        <v-btn
                            icon="mdi-delete"
                            size="small"
                            variant="text"
                            color="error"
                            @click="eliminarComentario(comentario.id)"
                        />
                    </template>
                </v-list-item>
            </v-list> -->
        
            <CommentItem
                v-for="comentario in comentarios"
                :key="comentario.id"
                :comentario="comentario"
                @delete="eliminarComentario"
            />
        </v-card>
        <v-alert v-else type="info" variant="tonal">
            No hay comentarios todavía
        </v-alert>
    </div>
</template>


<script setup>
import { ref, onMounted, watch } from 'vue'
import commentService from '@/services/comment.service'
import CommentItem from './CommentItem.vue'

const props = defineProps({
  taskId:{
    type:Number,
    required:true
  }
})

const comentarios = ref([])
const nuevoComentario = ref('')
const loading = ref(false)

// ================================
// CARGAR COMENTARIOS
// ================================
const cargarComentarios = async()=>{
    try{
        const response = await commentService.getByTask(props.taskId)
        comentarios.value = response.data
    } catch(error){
        console.error(
            'Error cargando comentarios',
            error
        )
    }
}

// ================================
// CREAR COMENTARIO
// ================================
const agregarComentario = async()=>{
    if(!nuevoComentario.value.trim())
        return
    try{
        loading.value=true

        await commentService.create({
            contenido:nuevoComentario.value,
            tarea:props.taskId
        })

        nuevoComentario.value=''
        await cargarComentarios()
    } catch(error){
        console.error(
            'Error creando comentario',
            error
        )
    } finally{
        loading.value=false
  }
}

// ================================
// ELIMINAR
// ================================
const eliminarComentario = async(id)=>{
    try{
        await commentService.delete(id)
        await cargarComentarios()
    } catch(error){

        console.error(
        'Error eliminando comentario',
        error
        )
    }
}

// ================================
// FORMATO FECHA
// ================================
const formatDate=(date)=>{
  if(!date)
    return ''

  return new Date(date)
    .toLocaleString('es-MX')
}

// cargar cuando inicia
onMounted(()=>{
  cargarComentarios()
})

// por si cambia la tarea abierta
watch(
  ()=>props.taskId,
  ()=>{
    cargarComentarios()
  }
)
</script>