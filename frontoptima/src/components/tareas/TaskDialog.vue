<template>
  <v-dialog
    :model-value="modelValue"
    max-width="900"
    persistent
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <v-card rounded="lg">

      <v-toolbar flat color="primary">
        <v-toolbar-title>
          {{ isEdit ? 'Editar tarea' : 'Nueva tarea' }}
        </v-toolbar-title>

        <v-spacer/>

        <v-btn
          icon="mdi-close"
          variant="text"
          @click="$emit('update:modelValue', false)"
        />
      </v-toolbar>

      <v-card-text>

        <TaskForm
          :task="task"
          @save="guardar"
          @cancel="$emit('update:modelValue', false)"
        />

      </v-card-text>

    </v-card>
  </v-dialog>
</template>

<script setup>

import { computed } from 'vue'
import TaskForm from './TaskForm.vue'

const props = defineProps({

  modelValue:Boolean,

  task:Object

})

const emit = defineEmits([
    'update:modelValue',
    'save'
])

const isEdit = computed(()=>!!props.task?.id)

function guardar(data){

    emit('save',data)

    emit('update:modelValue',false)

}

</script>