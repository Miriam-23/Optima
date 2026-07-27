<template>

    <v-card
    class="chat-window"
    elevation="18"
    rounded="xl"
    >

        <!-- ================= HEADER ================= -->

        <ChatHeader />

        <v-divider />

        <!-- ================= HISTORIAL ================= -->

        <ChatHistory />

        <v-divider />

        <!-- ================= MENSAJES ================= -->

        <div class="messages-wrapper">

            <ChatMessages />
            <ChatLoader v-if="store.loading" />

        </div>

        <v-divider />

        <!-- ================= INPUT ================= -->

        <ChatInput />

    </v-card>

</template>

<script setup>

import { useChatbotStore } from '@/stores/chatbot'
import ChatHeader from './ChatHeader.vue'
import ChatHistory from './ChatHistory.vue'
import ChatMessages from './ChatMessages.vue'
import ChatLoader from './ChatLoader.vue'
import ChatInput from './ChatInput.vue'

const store = useChatbotStore()

</script>

<style scoped>
.chat-window{
    position:absolute;
    right:0;
    bottom:52px;
    width:310px;
    height:490px;
    display:flex;
    flex-direction:column;
    overflow:hidden;
    background:white;
    border:1px solid rgba(0,0,0,.05);
}

/* Zona central */
.messages-wrapper{
    flex:1;
    overflow:hidden;
    display:flex;
    flex-direction:column;
    background:#fafafa;
}

@media (max-width:600px){
    .chat-window{
        width:100vw;
        height:100vh;
        right:0;
        bottom:0;
        border-radius:0 !important;
    }
}

</style>