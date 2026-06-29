import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from '@/stores/auth.js'

import MainLayout from '@/layouts/MainLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

import LoginView from '@/views/auth/LoginViews.vue'
import RegisterView from '@/views/auth/RegisterViews.vue'
import DashboardView from '@/views/dashboard/DashboardViews.vue'
import ProyectosView from '@/views/proyectos/ProyectosViews.vue'
import TareasView from '@/views/tareas/TareasViews.vue'
import UsuariosView from '@/views/usuarios/UsuariosViews.vue'
import ReportesView from '@/views/reportes/ReportesViews.vue'
import ConfiguracionView from '@/views/configuracion/ConfiguracionViews.vue'

const routes = [
  {
    path: '/',
    redirect: '/login',
  },

  {
    path: '/',
    component: AuthLayout,
    children: [
      {
        path: 'login',
        component: LoginView,
      },
      {
        path: 'register',
        component: RegisterView,
      },
    ],
  },

  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: 'dashboard',
        component: DashboardView,
      },
      {
        path: 'proyectos',
        component: ProyectosView,
      },
      {
        path: 'tareas',
        component: TareasView,
      },
      {
        path: 'usuarios',
        component: UsuariosView,
      },
      {
        path: 'reportes',
        component: ReportesView,
      },
      {
        path: 'configuracion',
        component: ConfiguracionView,
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.path !== '/login' && !auth.isAuthenticated) {
    return '/login'
  }

  if (to.path === '/login' && auth.isAuthenticated) {
    return '/dashboard'
  }
})
export default router
