<template>
  <v-dialog v-model="model" max-width="500">

    <v-card>

      <!-- HEADER -->
      <v-card-title>
        Asignar miembro al proyecto
      </v-card-title>

      <v-card-text>

        <!-- USUARIO -->
        <v-select
          v-model="form.usuario"
          :items="usuarios"
          item-title="username"
          item-value="id"
          label="Usuario"
          :loading="loadingUsers"
          class="mb-3"
        />

        <!-- ROL -->
        <v-select
          v-model="form.rol"
          :items="roles"
          item-title="nombre"
          item-value="id"
          label="Rol"
          :loading="loadingRoles"
          class="mb-3"
        />

        <!-- ERROR -->
        <v-alert
          v-if="error"
          type="error"
          class="mb-3"
        >
          {{ error }}
        </v-alert>

      </v-card-text>

      <!-- ACTIONS -->
      <v-card-actions>

        <v-spacer />

        <v-btn
          variant="text"
          @click="close"
        >
          Cancelar
        </v-btn>

        <v-btn
          color="primary"
          :loading="loading"
          @click="guardar"
        >
          Guardar
        </v-btn>

      </v-card-actions>

    </v-card>

  </v-dialog>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import userService from '@/services/user.service'
import roleService from '@/services/role.service'
import teamService from '@/services/team.service'

const props = defineProps({
  modelValue: Boolean,
  projectId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'saved'])

/* dialog v-model */
const model = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

/* estado */
const usuarios = ref([])
const roles = ref([])

const loadingUsers = ref(false)
const loadingRoles = ref(false)
const loading = ref(false)

const error = ref(null)

/* form */
const form = ref({
  usuario: null,
  rol: null
})

/* cargar usuarios */
const loadUsers = async () => {

  loadingUsers.value = true

  try {
    const res = await userService.getAll()
    usuarios.value = res.data
  } catch (err) {
    console.error(err)
  } finally {
    loadingUsers.value = false
  }
}

/* cargar roles */
const loadRoles = async () => {

  loadingRoles.value = true

  try {
    const res = await roleService.getAll()
    roles.value = res.data
  } catch (err) {
    console.error(err)
  } finally {
    loadingRoles.value = false
  }
}

/* guardar */
const guardar = async () => {

  error.value = null
  loading.value = true

  try {

    await teamService.create({
      usuario: form.value.usuario,
      rol: form.value.rol,
      proyecto: props.projectId
    })

    emit('saved')
    close()

  } catch (err) {

    if (err.response?.status === 400) {
      error.value = 'Este usuario ya está asignado a este proyecto con este rol'
    } else {
      error.value = 'Error al asignar miembro'
    }

  } finally {
    loading.value = false
  }
}

/* cerrar */
const close = () => {
  emit('update:modelValue', false)

  form.value.usuario = null
  form.value.rol = null
  error.value = null
}

onMounted(() => {
  loadUsers()
  loadRoles()
})
</script>