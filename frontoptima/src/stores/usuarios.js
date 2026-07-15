import { defineStore } from 'pinia'
import authService from '@/services/auth.service'


export const useUsuarioStore = defineStore('usuario', {
    state:()=>({
        usuario:null,
        loading:false,
        error:null
    }),


    getters:{
        nombreUsuario:(state)=>{
            return state.usuario?.username || ''
        },

        avatar:(state)=>{
            return state.usuario?.avatar_url || ''
        }
    },
    
    actions:{
        async cargarPerfil(){
            try{
                this.loading=true
                const response = await authService.obtenerPerfil()
                console.log("PERFIL API:", response.data)
                this.usuario=response.data

            }catch(error){

                this.error=error

            }finally{

                this.loading=false

            }
        },

        async actualizarPerfil(datos){
            try{
                const response = await authService.actualizarPerfil(datos)
                console.log("PERFIL API:", response.data)
                this.usuario=response.data

            }catch(error){
                this.error=error
            }
        }   
    }
})