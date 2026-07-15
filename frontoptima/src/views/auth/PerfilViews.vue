<!-- <template>
    <v-container fluid>

        <v-row>
            <v-col cols="12" md="4">
                <PerfilCard @editar="dialog=true" />
            </v-col>

            <v-col cols="12" md="8">
                <InforPersonal/>
            </v-col>
        </v-row>

    </v-container>
</template>


<script setup>
import { ref,onMounted } from 'vue'
import { useUsuarioStore } from '@/stores/usuarios'
import PerfilCard from '@/components/perfil/PerfilCard.vue'
import InforPersonal from '@/components/perfil/InforPersonal.vue'


const store = useUsuarioStore()
const dialog=ref(false)

onMounted(()=>{
    store.cargarPerfil()
})

</script> -->

<template>

<v-container fluid>

<v-row>


<v-col
cols="12"
md="4"
>

<PerfilCard
@editar="dialogEditar=true"
/>

</v-col>



<v-col
cols="12"
md="8"
>

<InforPersonal/>

</v-col>


</v-row>



<EditPerfilDialog
v-model="dialogEditar"
/>


</v-container>

</template>


<script setup>

import { ref,onMounted } from 'vue'
import { useUsuarioStore } from '@/stores/usuarios'
import PerfilCard from '@/components/perfil/PerfilCard.vue'
import InforPersonal from '@/components/perfil/InforPersonal.vue'
import EditPerfilDialog from '@/components/perfil/EditPerfilDialog.vue'

const store = useUsuarioStore()
const dialogEditar = ref(false)

onMounted(()=>{
    store.cargarPerfil()
})
</script>