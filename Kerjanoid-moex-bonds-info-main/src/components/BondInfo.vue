<template>
  <section>
    <p>{{ currentIsin }}</p>
  </section>
</template>

<script setup lang="ts">
import { computed } from "vue"
import { useRoute } from "vue-router"
const route = useRoute()

const currentIsin = computed(() => route.params.isin)
</script>

<style scoped lang="scss"></style>
