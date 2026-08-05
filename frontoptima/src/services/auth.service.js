import api from './api'

export default {

    obtenerPerfil(){
        return api.get('/auth/me/')
    },


    actualizarPerfil(data){
        return api.patch('/auth/me/', data)
    },

    forgotPassword(email) {
        return api.post("/auth/password-reset/", {
            email
        })
    },

    resetPassword(data) {
        return api.post("/auth/password-reset/confirm/", data)
    },

}