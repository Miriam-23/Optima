import api from './api'

export default {

    getAll(params = {}) {
        return api.get('/api/team/', {params})
    },

    getByProject(projectId) {
        return api.get('/api/team/', {
            params:{proyecto: projectId}
        })
    },

    create(data){
        return api.post('/api/team/', data)
    },

    delete(id){
        return api.delete(`/api/team/${id}/`)
    }
}