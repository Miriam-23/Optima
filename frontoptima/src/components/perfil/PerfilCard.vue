<template>
    <v-card class="pa-6" rounded="xl" elevation="2">

        <div v-if="!usuario">

            <v-progress-circular
                indeterminate
                color="primary"
            />

            <p class="mt-3">
                Cargando perfil...
            </p>

        </div>

        <div v-else class="text-center">

            <v-avatar size="120">
                <v-img :src="usuario?.avatar_url" />
            </v-avatar>

            <h2 class="mt-4">
                {{ usuario?.username }}
            </h2>

            <v-chip class="mt-3"
                :color="usuario.is_active ? 'green':'red'"
                variant="tonal"
            >
                {{ usuario?.is_active ? 'Activo':'Inactivo' }}
            </v-chip>

            <v-divider class="my-6"/>

            <v-btn
                color="primary"
                block
                prepend-icon="mdi-account-edit"
                @click="$emit('editar')"
            >
                Editar perfil
            </v-btn>

        </div>

    </v-card>
</template>


<script setup>

import { computed } from 'vue'
import { useUsuarioStore } from '@/stores/usuarios'


defineEmits([
    'editar'
])


const store = useUsuarioStore()
const usuario = computed(()=>store.usuario)


</script>