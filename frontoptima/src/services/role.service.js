import api from './api'

export default {

    getAll() {
        return api.get('/roles/')
    },

    getById(id) {
        return api.get(`/roles/${id}/`)
    }

}