import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'dashboard',
        component: () => import("@/views/DashboardSupervision.vue"),
    }, 
    {
        path: '/index.html',
        name: 'dashboard',
        component: () => import("@/views/DashboardSupervision.vue"),
    },
    {
        path: '/add_agents_to_campaign',
        name: 'add_agents_to_campaign',
        component: () => import("@/views/AddAgentsToCampaign.vue"),
    },
]

const router = createRouter({
    history: createWebHistory("/static/omnileads-ui-supervision/"),
    routes
})

export default router
