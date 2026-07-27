<template>

    <div class="history">

        <div
            class="history-header"
            @click="store.toggleHistory()"
        >

            <div class="d-flex align-center">

                <v-icon class="mr-2">
                    {{ store.historyOpen? 'mdi-chevron-down' : 'mdi-chevron-right' }}
                </v-icon>

                <span>Historial</span>

            </div>

            <span class="text-caption">{{ store.history.length }}</span>

        </div>

        <v-expand-transition>

            <div
                v-if="store.historyOpen"
                class="history-body"
            >

                <v-list density="compact">

                    <v-list-item
                        v-for="conversation in store.history"
                        :key="conversation.id"
                        rounded="lg"
                        @click="store.loadConversation(conversation.id)"
                    >

                        <template #prepend>

                            <v-icon>mdi-chat-outline</v-icon>

                        </template>

                        <v-list-item-title>
                            {{ conversation.projectName }}
                        </v-list-item-title>

                        <v-list-item-subtitle>
                            {{ conversation.lastMessage }}
                        </v-list-item-subtitle>

                        <v-list-item-subtitle>
                            {{ formatDate(conversation.createdAt) }}
                        </v-list-item-subtitle>

                    </v-list-item>

                </v-list>

            </div>

        </v-expand-transition>

    </div>

</template>

<script setup>
import { useChatbotStore } from '@/stores/chatbot'

const store = useChatbotStore()

function formatDate(date){

    return new Date(date).toLocaleDateString()

}

</script>

<style scoped>
.history{
    background:white;
}

.history-header{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:12px 16px;
    cursor:pointer;
    user-select:none;
    transition:.25s;
}

.history-header:hover{
    background:#f5f5f5;
}

.history-body{
    max-height:180px;
    overflow-y:auto;
    border-top:1px solid rgba(0,0,0,.06);
}

.history-body::-webkit-scrollbar{
    width:6px;
}

.history-body::-webkit-scrollbar-thumb{
    border-radius:10px;
    background:#d0d0d0;
}

</style>