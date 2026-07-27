<template>

    <div
        class="bubble-wrapper"
        :class="isUser ? 'justify-end' : 'justify-start'"
    >

        <!-- Avatar IA -->

        <v-avatar
            v-if="!isUser"
            size="38"
            color="primary"
            class="mr-3 mt-1"
        >
        <v-icon color="white">
            mdi-robot-outline
        </v-icon>
        </v-avatar>

        <!-- Burbuja -->

        <div
            class="bubble"
            :class="isUser ? 'user-bubble' : 'assistant-bubble'"
        >

            <div class="message">
                {{ message.content }}
            </div>

            <div class="time">
                {{  formattedTime  }}
            </div>

        </div>

    </div>

</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({

  message:{
    type:Object,
    required:true
  }

})

const isUser = computed(() => props.message.role === 'user')

const formattedTime = computed(() => {

    return new Date(props.message.createdAt)
        .toLocaleTimeString([],{
            hour:'2-digit',
            minute:'2-digit'
        })

})

</script>

<style scoped>
.bubble-wrapper{
    display:flex;
    align-items:flex-end;
    animation:fadeUp .25s ease;
}

/* ---------- Burbuja ---------- */
.bubble{
    max-width:75%;
    padding:12px 16px;
    border-radius:18px;
    word-break:break-word;
    white-space:pre-wrap;
    box-shadow:0 3px 8px rgba(0,0,0,.08);
}

/* Usuario */
.user-bubble{
    background:rgb(var(--v-theme-primary));
    color:white;
    border-bottom-right-radius:6px;
}

/* IA */
.assistant-bubble{
    background:white;
    color:rgb(var(--v-theme-on-surface));
    border:1px solid rgba(0,0,0,.08);
    border-bottom-left-radius:6px;
}

/* Texto */
.message{
    line-height:1.55;
    font-size:.95rem;
}

/* Hora */
.time{
    margin-top:8px;
    font-size:.72rem;
    opacity:.65;
    text-align:right;
}

/* Animación */

@keyframes fadeUp{

    from{
        opacity:0;
        transform:translateY(12px);
    }

    to{
        opacity:1;
        transform:translateY(0);
    }
}

</style>