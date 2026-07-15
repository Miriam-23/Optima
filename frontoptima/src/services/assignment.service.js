import api from './api'

export default {

  crearAsignacion(data){
    return api.post('/api/assignments/', data)
  },

  eliminarAsignacion(id){
    return api.delete( `/api/assignments/${id}/`)
  },

  listarAsignaciones(){
    return api.get('/api/assignments/')
  }
}