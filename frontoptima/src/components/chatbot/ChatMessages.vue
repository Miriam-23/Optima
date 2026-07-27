<template>

    <div
        ref="messagesContainer"
        class="messages-container"
    >

        <!-- Estado vacío -->

        <div
            v-if="store.messages.length === 0"
            class="empty-state"
        >

            <v-icon size="52" color="primary">mdi-robot-outline</v-icon>

            <h3>OptimaBot</h3>
            <p>¿En qué puedo ayudarte hoy?</p>

        </div>

        <!-- Conversación -->

        <template v-else>

            <ChatBubble
                v-for="message in store.messages"
                :key="message.id"
                :message="message"
            />

        </template>

    </div>

</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { useChatbotStore } from '@/stores/chatbot'
import ChatBubble from './ChatBubble.vue'

const store = useChatbotStore()
const messagesContainer = ref(null)

async function scrollBottom(){

    await nextTick()

    if(!messagesContainer.value) return

    messagesContainer.value.scrollTop =
        messagesContainer.value.scrollHeight

}

watch(
    () => store.messages.length,

    () => {

        scrollBottom()

    }

)

</script>

<style scoped>

.messages-container{
    flex:1;
    overflow-y:auto;
    padding:18px;
    display:flex;
    flex-direction:column;
    gap:14px;
    scroll-behavior:smooth;
}

/* Scroll */
.messages-container::-webkit-scrollbar{
    width:6px;
}

.messages-container::-webkit-scrollbar-thumb{
    background:#c7c7c7;
    border-radius:10px;
}

.messages-container::-webkit-scrollbar-track{
    background:transparent;
}

/* Estado vacío */
.empty-state{
    height:100%;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    text-align:center;
    padding:32px;
}

.empty-state h3{
    margin-top:18px;
    margin-bottom:8px;
    font-size:1.25rem;
    font-weight:700;
}

.empty-state p{
    margin-bottom:10px;
    font-size:1rem;
    color:rgb(var(--v-theme-on-surface));
}

.empty-state span{
    color:#7a7a7a;
    font-size:.90rem;
    line-height:1.5;
    max-width:280px;
}

</style>