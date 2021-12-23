import { h, resolveComponent } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'

import DefaultLayout from '@/layouts/DefaultLayout'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: DefaultLayout,
    redirect: '/dashboard',
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () =>
          import(/* webpackChunkName: "dashboard" */ '@/views/Dashboard.vue'),
      },
    ],
  },
  {
    path: '/pages',
    name: 'Pages',
    component: {
      render() {
        return h(resolveComponent('router-view'))
      },
    },
    children: [
      {
        path: 'login',
        name: 'Login',
        component: () => import('@/views/pages/Login'),
      },
      {
        path: 'register',
        name: 'Register',
        component: () => import('@/views/pages/Register'),
      },
    ],
  },
  {
    path: '/Customers',
    name: 'Customers',
    component: DefaultLayout,
    children: [
      {
        path: 'customer',
        name: 'Customer Lists',
        component: () => import('@/views/Customers/CustomerList'),
      },
      {
        path: 'customer',
        name: 'New Customer',
        component: () => import('@/views/Customers/CustomerList'),
      },
    ],
  },
  {
    path: '/Users',
    name: 'Users',
    component: DefaultLayout,
    children: [
      {
        path: 'user',
        name: 'User',
        component: () => import('@/views/Users/UserList'),
      },
    ],
  },
  {
    path: '/Disbursements',
    name: 'Disbursements',
    component: DefaultLayout,
    children: [
      {
        path: 'disbursed',
        name: 'Disbursed',
        component: () => import('@/views/Disbursements/Disbursed'),
      },
    ],
  },
]
const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
  scrollBehavior() {
    // always scroll to top
    return { top: 0 }
  },
})

export default router
