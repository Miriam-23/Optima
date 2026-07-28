import api from "./api"

class ChatbotService {

    /**Envía un mensaje al asistente*/
    async sendMessage(message, context = {}) {

        const payload = {
            message,
            context

        }

        const { data } = await api.post("api/chat/", payload)
        return data

    }

    /**Obtiene el historial desde el backend**/
    async getHistory() {

        const { data } = await api.get("/chat/history/")
        return data

    }

    /**Obtiene una conversación*/
    async getConversation(id) {

        const { data } = await api.get(`/chat/history/${id}/`)
        return data

    }

    /**Elimina una conversación*/
    async deleteConversation(id) {

        return api.delete(`/chat/history/${id}/`)

    }

}

export default new ChatbotService()
