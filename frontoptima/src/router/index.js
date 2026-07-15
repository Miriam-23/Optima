import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from '@/stores/auth.js'

import MainLayout from '@/layouts/MainLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

import LoginView from '@/views/auth/LoginViews.vue'
import RegisterView from '@/views/auth/RegisterViews.vue'
import VerifyAccountView from '@/views/auth/VerifyAccountView.vue'
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
        name:'login',
        component: LoginView,
        meta: {
          public: true
        }
      },
      {
        path: 'register',
        name:'register',
        component: RegisterView,
        meta: {
          public: true
        }
      },
      {
        path: 'verificar/:token',
        name: 'verify-account',
        component: VerifyAccountView,
        meta: {
          public: true
        }
      },
    ],
  },
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: 'dashboard',
        name:'dasboard',
        component: DashboardView,
      },
      {
        path: 'proyectos',
        name:'proyectos',
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
        name:'tareas',
        component: TareasView,
      },
      {
        path: 'perfil',
        name:'perfil',
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

  const authRequired = !to.meta.public

  if (authRequired && !auth.isAuthenticated) {
    return '/login'
  }

  if (to.meta.public && auth.isAuthenticated) {
    return '/dashboard'
  }

})
export default router
