import api from './api'

export default {

    getAll() {
        return api.get('/users/')
    },

    getById(id) {
        return api.get(`/users/${id}/`)
    }

}