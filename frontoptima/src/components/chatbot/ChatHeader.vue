<template>

    <div class="chat-header">

        <!-- Información del asistente -->
        <div class="assistant-info">

            <v-avatar color="white" size="36">
                <v-icon color="primary" size="28">mdi-robot-outline</v-icon>
            </v-avatar>

            <div class="assistant-text">

                <div class="assistant-name">OptimaBot</div>

                <div class="assistant-status">
                
                    <span class="status-dot" /> 
                    En línea

                </div>

            </div>

        </div>

    </div>

</template>

<script setup>
import { useChatbotStore } from '@/stores/chatbot'

const store = useChatbotStore()

</script>

<style scoped>
.chat-header{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:16px 18px;
    background:linear-gradient(
        135deg,
        rgb(var(--v-theme-primary)),
        rgb(var(--v-theme-primary-darken-1))
    );
    color:white;
}

/* Información */
.assistant-info{
    display:flex;
    align-items:center;
    gap:14px;
}

.assistant-text{
    display:flex;
    flex-direction:column;
}

.assistant-name{
    font-size:1rem;
    font-weight:700;
    line-height:1.2;
}

.assistant-status{
    display:flex;
    align-items:center;
    gap:6px;
    margin-top:2px;
    font-size:.82rem;
    opacity:.95;
}

.status-dot{
    width:8px;
    height:8px;
    border-radius:50%;
    background:#4CAF50;
    box-shadow:0 0 6px #4CAF50;
}

/* Acciones */
.header-actions{
    display:flex;
    align-items:center;
    gap:4px;
}

.header-actions .v-btn{
    transition:.25s;
}

.header-actions .v-btn:hover{
    background:rgba(255,255,255,.12);
    transform:scale(1.05);
}

</style>