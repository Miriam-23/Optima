<template>

    <div class="loader-wrapper">

        <v-avatar size="38" color="primary">
            <v-icon color="white">mdi-robot-outline</v-icon>
        </v-avatar>

        <div class="loader-bubble">

            <div class="loader-title">
                Optima Assistant
            </div>

            <div class="loader-subtitle">
                Pensando...
            </div>

            <div class="dots">
                <span></span>
                <span></span>
                <span></span>
            </div>

        </div>

    </div>

</template>

<style scoped>

.loader-wrapper{
    display:flex;
    align-items:flex-end;
    gap:12px;
    margin-top:8px;
    animation:fadeIn .25s ease;
}

.loader-bubble{
    background:white;
    border-radius:18px;
    border-bottom-left-radius:6px;
    padding:14px 18px;
    border:1px solid rgba(0,0,0,.08);
    box-shadow:0 3px 10px rgba(0,0,0,.05);
}

.loader-title{
    font-weight:600;
    font-size:.92rem;
}

.loader-subtitle{
    color:#777;
    margin-top:2px;
    font-size:.82rem;
}

.dots{
    display:flex;
    gap:6px;
    margin-top:10px;
}

.dots span{
    width:8px;
    height:8px;
    border-radius:50%;
    background:rgb(var(--v-theme-primary));
    animation:bounce 1.2s infinite ease-in-out;
}

.dots span:nth-child(2){
    animation-delay:.2s;
}

.dots span:nth-child(3){
    animation-delay:.4s;
}

@keyframes bounce{

    0%,80%,100%{
        transform:scale(.6);
        opacity:.5;
    }

    40%{
        transform:scale(1);
        opacity:1;
    }

}

@keyframes fadeIn{
    from{
        opacity:0;
        transform:translateY(8px);
    }

    to{
        opacity:1;
        transform:none;
    }

}

</style>