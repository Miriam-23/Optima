<template>

    <v-card
        class="pa-6"
        rounded="xl"
        elevation="2"
    >


    <h3 class="mb-5">
        Información personal
    </h3>


        <v-list v-if="usuario">

            <v-list-item>

                <template #title>
                    ID Usuario
                </template>

                <template #subtitle>
                    {{ usuario.id }}
                </template>

            </v-list-item>

            <v-list-item>

                <template #title>
                    Username
                </template>

                <template #subtitle>
                    {{ usuario.username }}
                </template>

            </v-list-item>

            <v-list-item>

                <template #title>
                    Correo electrónico
                </template>

                <template #subtitle>
                    {{ usuario.email }}
                </template>

            </v-list-item>

            <v-list-item>

                <template #title>
                    Estado
                </template>

                <template #subtitle>

                    {{ usuario.is_active ? 'Activo':'Inactivo' }}

                </template>

            </v-list-item>

            <v-list-item>

                <template #title>
                    Fecha de registro
                </template>

                <template #subtitle>

                    {{ fechaRegistro }}

                </template>

            </v-list-item>

        </v-list>


        <v-progress-circular
            v-else
            indeterminate
            color="primary"
        />


    </v-card>

</template>


<script setup>
import { computed } from 'vue'
import { useUsuarioStore } from '@/stores/usuarios'


const store = useUsuarioStore()
const usuario = computed(()=>store.usuario)
const fechaRegistro = computed(()=>{

    if(!usuario.value)
        return ''


    return new Date(
        usuario.value.date_joined
    ).toLocaleDateString()

})


</script>