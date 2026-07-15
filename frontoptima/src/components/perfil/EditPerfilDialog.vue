<template>

<v-dialog
    v-model="dialog"
    max-width="500"
>

<v-card
    rounded="xl"
    class="pa-6"
>


<div class="d-flex align-center mb-5">

<v-icon
    color="primary"
    size="32"
>
    mdi-account-edit
</v-icon>


<div class="ml-3">

<h3>
Editar perfil
</h3>

<span class="text-medium-emphasis">
Actualiza tus datos personales
</span>

</div>

</div>



<v-text-field
    v-model="form.username"
    label="Nombre de usuario"
    prepend-inner-icon="mdi-account"
    variant="outlined"
/>



<v-text-field
    v-model="form.email"
    label="Correo electrónico"
    prepend-inner-icon="mdi-email-outline"
    variant="outlined"
    class="mt-4"
/>



<v-alert
    v-if="error"
    type="error"
    variant="tonal"
    class="mt-4"
>
{{ error }}
</v-alert>



<div class="d-flex justify-end mt-6">


<v-btn
    variant="text"
    @click="cerrar"
>
Cancelar
</v-btn>



<v-btn
    color="primary"
    class="ml-3"
    :loading="loading"
    @click="guardar"
>
Guardar cambios
</v-btn>


</div>


</v-card>

</v-dialog>

</template>



<script setup>

import { reactive, computed, watch, ref } from 'vue'
import { useUsuarioStore } from '@/stores/usuarios'

const store = useUsuarioStore()
const props = defineProps({

    modelValue:{
        type:Boolean,
        default:false
    }
})

const emit = defineEmits([
    'update:modelValue',
    'actualizado'
])

const dialog = ref(false)
const form = reactive({
    username:'',
    email:''
})

const loading = ref(false)
const error = ref(null)

/* Sincronizar dialog*/

watch(

()=>props.modelValue,

(value)=>{

    dialog.value=value

    if(value){

        cargarDatos()

    }

}

)



watch(

dialog,

(value)=>{

emit(
'update:modelValue',
value
)

}

)



const usuario = computed(()=>store.usuario)



const cargarDatos=()=>{


if(!usuario.value)
return


form.username =
usuario.value.username


form.email =
usuario.value.email


}



/*
Guardar cambios
*/

const guardar=async()=>{


try{


loading.value=true

error.value=null



await store.actualizarPerfil({

username:form.username,

email:form.email

})



emit('actualizado')



cerrar()



}catch(e){

error.value=
"No fue posible actualizar el perfil"

}finally{

loading.value=false

}


}



const cerrar=()=>{

dialog.value=false

}



</script>