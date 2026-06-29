<template>
    <v-container>
        <v-chip variant="text" size="x-large" class="text-h6 font-weight-regular">
            <v-icon class="mr-2">mdi-cog</v-icon>
            Configuración
        </v-chip>
        
        <v-divider class="border-opacity-100 my-4" color="accent" />

        <v-row>
            <v-col cols="6">
                <v-card>
                    <v-card-title>Mi Panel</v-card-title>
                    <v-card-text>
                        <p>Bienvenido a tu espacio de configuración.</p>
                        <v-text-field
                            v-model="usuario.nombre"
                            label="Nombre"
                            prepend-icon="mdi-account"
                        />
                        <v-text-field
                            v-model="usuario.email"
                            label="Correo electrónico"
                            prepend-icon="mdi-email"
                        />
                        <v-switch
                            v-model="usuario.notificaciones"
                            label="Activar notificaciones"
                            inset
                        />
                        <v-btn color="primary" class="mt-4" @click="guardar">Guardar cambios</v-btn>
                    </v-card-text>
                </v-card>
            </v-col>

            <v-divider class="border-opacity-100 my-4" color="accent" vertical/>

            <v-col cols="6">
                <v-card>
                    <v-card-title>Configuracion de la página</v-card-title>
                    <v-card-text>
                        <v-row align="center" justify="space-between">
                        <v-chip variant="text" size="x-large">Idioma:</v-chip>
                        <v-select
                            v-model="idioma"
                            :items="idiomas"
                            label="Selecciona idioma"
                            variant="outlined"
                            density="compact"
                            style="max-width: 200px;"
                        />
                        </v-row>

                        <v-divider class="my-4" />

                        <!-- Fuente o tamaño (opcional) -->
                        <v-row align="center" justify="space-between">
                        <v-chip>Tamaño de fuente:</v-chip>
                        <v-slider
                            v-model="tamanioFuente"
                            :min="12"
                            :max="24"
                            step="1"
                            show-ticks
                            thumb-label
                            style="max-width: 300px;"
                        />
                        </v-row>

                        <v-divider class="my-4" />

                        <!-- Accesibilidad (ejemplo opcional) -->
                        <v-switch
                        v-model="modoAccesible"
                        label="Modo accesible (alto contraste)"
                        inset
                        />

                        <v-btn color="primary" class="mt-4" @click="guardar">Guardar cambios</v-btn>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <v-divider class="border-opacity-100 my-4" color="accent" />

        <v-row>
            <v-col cols="6">
                <v-card >
                    <v-card-title><v-icon>mdi-water</v-icon>Colores de Tema</v-card-title>
                    <v-card-text>
                        <v-row>
                        <TemaColores color="bg-primary"><h5>Primario</h5></TemaColores>
                        <TemaColores color="bg-secondary"><h5>Secundario</h5></TemaColores>
                        <TemaColores color="bg-success"><h5>Exito</h5></TemaColores>
                        <TemaColores color="bg-error"><h5>Error</h5></TemaColores>
                        <TemaColores color="bg-warning"><h5>Advertencia</h5></TemaColores>
                        <TemaColores color="bg-info"><h5>Información</h5></TemaColores>
                        <TemaColores color="bg-accent"><h5>Acentuación</h5></TemaColores>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

    </v-container>
</template>

<script setup>
import { ref } from 'vue'
//import TemaColores from '@/theme/TemaColores.vue'

const usuario = ref({
  nombre: '',
  email: '',
  notificaciones: false,
})

function guardar() {
  console.log('Datos guardados:', usuario.value)
  // Aquí puedes enviar la info al backend o mostrar un snackbar
}

// Idiomas disponibles
const idiomas = ['Español', 'Inglés', 'Francés']
const idioma = ref('Español')

// Fuente
const tamanioFuente = ref(16)

// Accesibilidad
const modoAccesible = ref(false)

</script>
