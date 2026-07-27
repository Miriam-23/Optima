<template>

  <div class="chat-input">

        <v-textarea
            v-model="message"
            class="input"
            variant="solo-filled"
            density="comfortable"
            rows="1"
            auto-grow
            max-rows="5"
            hide-details
            placeholder="Escribe un mensaje..."
            @keydown.enter.exact.prevent="send"
        />

        <v-btn
            :icon="store.loading ? 'mdi-stop' : 'mdi-send'"
            :color="store.loading ? 'error' : 'primary'"
            :disabled="!message.trim() && !store.loading"
            elevation="2"
            @click="store.loading ? stop() : send()"
        />

  </div>

</template>

<script setup>
import { ref } from 'vue'
import { useChatbotStore } from '@/stores/chatbot'

const store = useChatbotStore()
const message = ref('')

async function send(){
    if(store.loading) return
    if(!message.value.trim()) return
    const text = message.value.trim()
    message.value=''
    await store.sendMessage(text)
}

function stop(){
    store.stopResponse()
}

</script>

<style scoped>
.chat-input{
    display:flex;
    align-items:flex-end;
    gap:12px;
    padding:16px;
    background:white;
}

.input{
    flex:1;
}

:deep(.v-field){
    border-radius:18px;
}

</style>