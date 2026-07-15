import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from '@/stores/auth.js'

import MainLayout from '@/layouts/MainLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

import LoginView from '@/views/auth/LoginViews.vue'
import RegisterView from '@/views/auth/RegisterViews.vue'
import DashboardView from '@/views/dashboard/DashboardViews.vue'
import ProyectosView from '@/views/proyectos/ProyectosViews.vue'
import TareasView from '@/views/tareas/TareasViews.vue'
import PerfilView from '@/views/auth/PerfilViews.vue'
import ProyectoDetalleView from '@/views/proyectos/ProyectoDetailsViews.vue'

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
        path: 'proyectos/:id',
        name: 'proyecto-detalle',
        component: ProyectoDetalleView,
        props: true
      },
      {
        path: 'tareas',
        component: TareasView,
      },
      {
        path: 'perfil',
        component: PerfilView,
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
  const publicPages = ['/login', '/register']
  const authRequired = !publicPages.includes(to.path)

  if (authRequired && !auth.isAuthenticated) {
    return '/login'
  }

  if (publicPages.includes(to.path) && auth.isAuthenticated) {
    return '/dashboard'
  }

})
export default router
