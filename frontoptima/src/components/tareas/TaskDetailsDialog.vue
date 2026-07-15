<template>
    <v-dialog v-model="dialog" max-width="800">
        <v-card v-if="task">
            <!-- HEADER -->
            <v-card-title class="d-flex justify-space-between align-center">

                <span>
                    {{ task.titulo }}
                </span>

                <v-btn
                    icon="mdi-close"
                    variant="text"
                    @click="dialog=false"
                />

            </v-card-title>

            <v-divider />

            <v-card-text>

                <!-- INFORMACIÓN -->
                <h3 class="mb-4">
                    Información
                </h3>

                <v-row>

                    <v-col cols="12" md="6">
                        <v-list density="compact">

                            <v-list-item>
                                <template #prepend>
                                    <v-icon>mdi-folder</v-icon>
                                </template>

                                <v-list-item-title>
                                    Proyecto
                                </v-list-item-title>

                                <v-list-item-subtitle>
                                    {{ task.nombre_proyecto }}
                                </v-list-item-subtitle>

                            </v-list-item>


                            <v-list-item>

                                <template #prepend>
                                    <v-icon>mdi-flag</v-icon>
                                </template>


                                <v-list-item-title>
                                    Prioridad
                                </v-list-item-title>

                                <v-list-item-subtitle>
                                    <v-chip
                                        size="small"
                                        :color="priorityColor(task.prioridad)"
                                    >
                                        {{ task.prioridad }}
                                    </v-chip>
                                </v-list-item-subtitle>

                            </v-list-item>

                        </v-list>
                    </v-col>

                    <v-col cols="12" md="6">
                        <v-list density="compact">
                            <v-list-item>

                                <template #prepend>
                                    <v-icon>mdi-progress-clock</v-icon>
                                </template>

                                <v-list-item-title>
                                    Estado
                                </v-list-item-title>

                                <v-list-item-subtitle>
                                    {{ task.nombre_estado }}
                                </v-list-item-subtitle>

                            </v-list-item>



                            <v-list-item>

                            <template #prepend>
                                <v-icon>
                                mdi-calendar
                                </v-icon>
                            </template>


                            <v-list-item-title>
                                Fecha límite
                            </v-list-item-title>


                            <v-list-item-subtitle>
                                {{ task.fecha_limite }}
                            </v-list-item-subtitle>


                            </v-list-item>


                        </v-list>
                    </v-col>

                </v-row>

                <!-- DESCRIPCIÓN -->
                <h3 class="mt-6 mb-3">
                    Descripción
                </h3>

                <v-card variant="tonal" class="pa-4">
                    {{ task.descripcion || 'Sin descripción' }}
                </v-card>

                <!-- RESPONSABLES -->
                <h3 class="mt-6 mb-3">
                    Responsables
                </h3>

                <v-chip
                    v-for="user in task.responsables"
                    :key="user.usuario_id"
                    class="mr-2"
                >
                    <v-icon start>mdi-account</v-icon>
                    {{ user.nombre }}

                </v-chip>

                <!-- COMENTARIOS -->
                <TaskComments class="mt-8" :task-id="task.id" />

            </v-card-text>
        </v-card>
    </v-dialog>
</template>



<script setup>
import { computed } from 'vue'
import TaskComments from './TaskComments.vue'

const props = defineProps({

  modelValue:{
    type:Boolean,
    default:false
  },

  task:{
    type:Object,
    default:null
  }

})

const emit = defineEmits(['update:modelValue'])

const dialog = computed({
    get(){return props.modelValue},

    set(value){emit('update:modelValue',value)}
})

const priorityColor = (priority)=>{
    switch(priority){
        case 'Alta':return 'error'
        case 'Media': return 'warning'
        case 'Baja': return 'success'
        default: return 'grey'

    }
}
</script>