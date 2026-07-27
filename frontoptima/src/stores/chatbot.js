import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatbotStore = defineStore('chatbot', () => {

    const open = ref(false)
    const loading = ref(false)
    const unread = ref(0)
    const messages = ref([])
    const history = ref([])
    const minimized = ref(false)
    const currentConversation = ref(null)
    const historyOpen = ref(false)

    let id = 1

    async function sendMessage(text){

        messages.value.push({
            id:id++,
            role:'user',
            content:text,
            createdAt:new Date()
        })
        
        loading.value=true
        
        try{
            await new Promise(resolve=>setTimeout(resolve,1500))

            messages.value.push({
                id:id++,
                role:'assistant',
                content:'Esta es una respuesta simulada de Optima Assistant.',
                createdAt:new Date()
            })
        }
        finally{
            loading.value=false
        }

    }

    function stopResponse(){

        loading.value=false

    }

    function toggle() {
        open.value = !open.value

        if (open.value) {
        unread.value = 0
        }
    }

    function close() {
        open.value = false
    }

    function openChat() {
        open.value = true
        unread.value = 0
    }


    function minimize() {
        minimized.value = !minimized.value
    }

    function toggleHistory(){

    historyOpen.value = !historyOpen.value

}

    function loadConversation(id){
        const conversation = history.value.find(c => c.id === id)
        if(!conversation) return
        currentConversation.value = conversation.id
        messages.value = [...conversation.messages]
    }

    function saveConversation(){
        if(messages.value.length === 0) return

        history.value.unshift({
            id:Date.now(),
            title:messages.value[0].content.substring(0,30),
            date:new Date(),
            messages:[...messages.value]
        })

    }

    return {
        open,
        loading,
        unread,
        messages,
        history,
        toggle,
        close,
        openChat,
        sendMessage,
        stopResponse,
        toggleHistory,
        loadConversation,
        saveConversation,
        minimize
    }

})