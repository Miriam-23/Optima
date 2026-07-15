<template>
  <v-menu
    v-model="menu"
    :close-on-content-click="false"
    location="bottom end"
    offset="8"
  >
    <template #activator="{ props }">
      <v-btn v-bind="props" icon class="position-relative">
        <v-icon>mdi-bell</v-icon>
        <span
          v-if="unreadCount > 0"
          class="notification-badge"
        >
          {{ unreadCount > 9 ? '9+' : unreadCount }}
        </span>
      </v-btn>
    </template>

    <v-card min-width="340" max-width="380" class="notification-panel">
      <v-card-title class="d-flex align-center justify-space-between px-4 pt-4 pb-2">
        <span class="text-subtitle-1 font-weight-bold">Notificaciones</span>
        <v-btn
          v-if="notifications.length"
          variant="text"
          size="small"
          color="primary"
          :loading="markingAllAsRead"
          @click="markAllAsRead"
        >
          Marcar todas como leídas
        </v-btn>
      </v-card-title>

      <v-divider />

      <div v-if="loading" class="py-8 d-flex justify-center">
        <v-progress-circular indeterminate color="primary" />
      </div>

      <div v-else-if="errorMessage" class="pa-4">
        <v-alert type="error" variant="tonal" border="start">
          {{ errorMessage }}
        </v-alert>
      </div>

      <div v-else-if="!notifications.length" class="pa-6 text-center">
        <v-icon size="36" color="primary" class="mb-3">mdi-bell-outline</v-icon>
        <div class="text-body-1 font-weight-medium">No tienes notificaciones</div>
        <div class="text-caption text-medium-emphasis mt-2">
          Las novedades aparecerán aquí cuando lleguen.
        </div>
      </div>

      <div v-else class="notification-list">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="notification-item"
          :class="{
            'notification-item--unread': !notification.leida,
            'notification-item--read': notification.leida
          }"
        >
          <div class="notification-item__icon">
            <v-icon :color="iconColor(notification.tipo)" size="20">
              {{ iconForType(notification.tipo) }}
            </v-icon>
          </div>

          <div class="notification-item__content">
            <div class="d-flex align-start justify-space-between">
              <div class="text-body-2 font-weight-medium">{{ notification.mensaje }}</div>
            </div>
            <div class="notification-item__meta mt-1">
              <span>{{ formatRelativeTime(notification.fecha_creacion) }}</span>
            </div>
          </div>
        </div>
      </div>
    </v-card>
  </v-menu>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import notificationsService from '@/services/notifications.service'

const menu = ref(false)
const notifications = ref([])
const loading = ref(false)
const markingAllAsRead = ref(false)
const errorMessage = ref('')

const unreadCount = computed(() => {
  return notifications.value.filter((item) => !item.leida).length
})

const loadNotifications = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await notificationsService.getAll()
    notifications.value = Array.isArray(response?.data) ? response.data : []
  } catch (error) {
    errorMessage.value = 'No fue posible cargar las notificaciones. Intenta nuevamente.'
    console.error('Error loading notifications:', error)
  } finally {
    loading.value = false
  }
}

const markAllAsRead = async () => {
  if (markingAllAsRead.value) return

  markingAllAsRead.value = true
  errorMessage.value = ''

  try {
    await notificationsService.markAllAsRead()
    notifications.value = notifications.value.map((item) => ({ ...item, leida: true }))
  } catch (error) {
    errorMessage.value = 'No fue posible marcar las notificaciones como leídas.'
    console.error('Error marking notifications as read:', error)
  } finally {
    markingAllAsRead.value = false
  }
}

const iconForType = (type) => {
  switch (type) {
    case 'tarea_asignada':
      return 'mdi-account-plus'
    case 'comentario_nuevo':
      return 'mdi-comment-text-outline'
    case 'tarea_vencida':
      return 'mdi-alert-circle-outline'
    case 'miembro_agregado':
      return 'mdi-account-group'
    default:
      return 'mdi-bell-outline'
  }
}

const iconColor = (type) => {
  switch (type) {
    case 'tarea_asignada':
      return 'primary'
    case 'comentario_nuevo':
      return 'info'
    case 'tarea_vencida':
      return 'error'
    case 'miembro_agregado':
      return 'success'
    default:
      return 'secondary'
  }
}

const formatRelativeTime = (value) => {
  if (!value) return ''

  const date = new Date(value)
  const diffMs = Date.now() - date.getTime()
  const diffMinutes = Math.floor(diffMs / 60000)

  if (diffMinutes < 1) return 'Ahora mismo'
  if (diffMinutes < 60) return `Hace ${diffMinutes} minuto${diffMinutes === 1 ? '' : 's'}`

  const diffHours = Math.floor(diffMinutes / 60)
  if (diffHours < 24) return `Hace ${diffHours} hora${diffHours === 1 ? '' : 's'}`

  const diffDays = Math.floor(diffHours / 24)
  if (diffDays < 7) return `Hace ${diffDays} día${diffDays === 1 ? '' : 's'}`

  const diffWeeks = Math.floor(diffDays / 7)
  return `Hace ${diffWeeks} semana${diffWeeks === 1 ? '' : 's'}`
}

onMounted(() => {
  loadNotifications()
})
</script>

<style scoped>
.notification-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  min-width: 18px;
  height: 18px;
  padding: 0 4px;
  border-radius: 999px;
  background: rgb(var(--v-theme-error));
  color: white;
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-panel {
  border-radius: 12px;
}

.notification-list {
  max-height: 360px;
  overflow-y: auto;
}

.notification-item {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  padding: 12px 14px;
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-item--unread {
  background: rgba(var(--v-theme-primary), 0.06);
}

.notification-item--read {
  opacity: 0.75;
}

.notification-item__icon {
  margin-top: 2px;
  flex-shrink: 0;
}

.notification-item__content {
  flex: 1;
  min-width: 0;
}

.notification-item__meta {
  font-size: 12px;
  color: rgba(var(--v-theme-on-surface), 0.64);
}
</style>
