import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import chatbotService from '@/services/chatbot.service'

export const useChatbotStore = defineStore('chatbot', () => {

    /* ===========================
       ESTADO
    =========================== */

    const open = ref(false)
    const minimized = ref(false)

    const loading = ref(false)
    const unread = ref(0)

    const history = ref([])
    const currentConversation = ref(null)
    const historyOpen = ref(false)

    const error = ref(null)
    const controller = ref(null)

    /* ===========================
       MENSAJES DE LA CONVERSACIÓN ACTUAL
    =========================== */

    const messages = computed(() => {

        const conversation = history.value.find(
            c => c.id === currentConversation.value
        )

        return conversation?.messages ?? []

    })

    /* ===========================
       CHAT
    =========================== */

    function toggle() {

        open.value = !open.value

        if (open.value) {
            unread.value = 0
        }

    }

    function openChat() {

        open.value = true
        unread.value = 0

        if (!currentConversation.value) {
            createConversation()
        }

    }

    function close() {

        open.value = false

    }

    function minimize() {

        minimized.value = !minimized.value

    }

    /* ===========================
       HISTORIAL
    =========================== */

    function toggleHistory() {

        historyOpen.value = !historyOpen.value

    }

    function createConversation(project = null) {

        const conversation = {
            id: Date.now(),
            title: "Nueva conversación",
            projectId: project?.id ?? null,
            projectName: project?.nombre ?? "General",
            createdAt: new Date(),
            lastMessage: "",
            messages: []
        }

        history.value.unshift(conversation)
        currentConversation.value = conversation.id

    }

    function loadConversation(id) {

        const exists = history.value.some(
            c => c.id === id
        )

        if (!exists) return

        currentConversation.value = id

    }

    /* ===========================
       MENSAJES
    =========================== */

    async function sendMessage(text) {

        if (loading.value) return

        if (!text.trim()) return

        let conversation = history.value.find(
            c => c.id === currentConversation.value
        )

        if (!conversation) {

            createConversation()

            conversation = history.value.find(
                c => c.id === currentConversation.value
            )

        }

        conversation.messages.push({
            id: Date.now(),
            role: "user",
            content: text,
            createdAt: new Date()
        })
        if (conversation.title === "Nueva conversación") {

            conversation.title =
                text.length > 35
                    ? text.substring(0, 35) + "..."
                    : text

        }

        conversation.lastMessage = text

        loading.value = true
        error.value = null

        try {

            const response = await chatbotService.sendMessage(text)

            conversation.messages.push({
                id: Date.now() + 1,
                role: "assistant",
                content: response.response,
                createdAt: new Date()
            })

            conversation.lastMessage = response.response

        }

        catch (err) {

            error.value = err

            conversation.messages.push({
                id: Date.now() + 2,
                role: "assistant",
                type: "error",
                content: "No fue posible contactar con Optima Assistant.",
                createdAt: new Date()
            })

        }

        finally {
            loading.value = false
        }

    }

    function stopResponse() {

        loading.value = false
        controller.value?.abort?.()

    }

    return {
        // Estado
        open,
        minimized,
        loading,
        unread,
        error,
        controller,
        // Conversaciones
        history,
        historyOpen,
        currentConversation,
        messages,
        // Acciones
        toggle,
        openChat,
        close,
        minimize,
        toggleHistory,
        createConversation,
        loadConversation,
        sendMessage,
        stopResponse
    }
})