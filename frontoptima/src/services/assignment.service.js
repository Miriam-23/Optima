import api from './api'

export default {

  crearAsignacion(data){
    return api.post('/assignments/', data)
  },

  eliminarAsignacion(id){
    return api.delete( `/assignments/${id}/`)
  },

  listarAsignaciones(){
    return api.get('/assignments/')
  }
}