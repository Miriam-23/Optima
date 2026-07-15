import api from './api'

export default {

    obtenerPerfil(){
        return api.get('/api/auth/me/')
    },


    actualizarPerfil(data){
        return api.patch('/api/auth/me/', data)
    }

}