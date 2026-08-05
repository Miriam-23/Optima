import api from './api'

export default {

    getAll(params = {}) {
        return api.get('/team/', {params})
    },

    getByProject(projectId) {
        return api.get('/team/', {
            params:{proyecto: projectId}
        })
    },

    create(data){
        return api.post('/team/', data)
    },

    delete(id){
        return api.delete(`/team/${id}/`)
    }
}