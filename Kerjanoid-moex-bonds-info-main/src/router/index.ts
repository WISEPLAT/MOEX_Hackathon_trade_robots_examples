import { createRouter, createWebHistory } from "vue-router"
import InitialInfo from "@/components/InitialInfo.vue"
import BondInfo from "@/components/BondInfo.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: InitialInfo
    },
    {
      path: "/:isin",
      name: "bond-info",
      component: BondInfo
    }
  ]
})

export default router
