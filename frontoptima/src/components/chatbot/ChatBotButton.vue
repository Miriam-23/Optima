<template>
    <div class="chatbot-container">

        <v-badge
            :content="store.unread"
            :model-value="store.unread > 0"
            color="error"
            floating
        >

            <v-btn
                class="chatbot-btn"
                color="primary"
                size="50"
                elevation="12"
                icon
                @click="store.toggle()"
            >
                <v-icon size="30">
                {{ store.open ? 'mdi-close' : 'mdi-robot-outline' }}
                </v-icon>
            </v-btn>

        </v-badge>

        <Transition name="chat">

        <ChatBotWindow v-if="store.open"/>

        </Transition>

    </div>
</template>

<script setup>
import { useChatbotStore } from '@/stores/chatbot'
import ChatBotWindow from './ChatBotWindow.vue'
const store = useChatbotStore()

</script>

<style scoped>
.chatbot-container{
    position:fixed;
    right:24px;
    bottom:24px;
    z-index:9999;
}

.chatbot-btn{
    transition:.25s;
}

.chatbot-btn:hover{
    transform:scale(1.08);
}

.chatbot-btn:active{
    transform:scale(.95);
}

/* Animación ventana */

.chat-enter-active,
.chat-leave-active{
    transition:all .30s ease;
}

.chat-enter-from,
.chat-leave-to{
    opacity:0;
    transform:translateY(30px) scale(.85);
}

.chat-enter-to,
.chat-leave-from{
    opacity:1;
    transform:translateY(0) scale(1);
}
</style>