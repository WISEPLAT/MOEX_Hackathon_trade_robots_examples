<template>
  <header class="header">
    <h1 class="header__title">MOEX Bonds info</h1>
  </header>
  <MainView>
    <Search></Search>
    <RouterView></RouterView>
  </MainView>
  <footer class="footer">
    <p class="footer__content">
      <a class="footer__link" href="https://github.com/kerjanoid" target="_blank" rel="noreferrer"
        >Kerjanoid</a
      >
      &#169; 2023
    </p>
  </footer>
</template>

<script setup lang="ts">
import { RouterView } from "vue-router"

import MainView from "@/views/MainView.vue"
import Search from "@/components/Search.vue"
</script>

<style lang="scss" scoped>
@import "@/assets/base.scss";
.header {
  padding: 20px;

  &__title {
    font-weight: bold;
    opacity: var(--bi-l-opacity);
  }
}

.footer {
  padding: 12px;

  &__content {
    font-weight: bold;
    opacity: var(--bi-l-opacity);
  }

  &__link {
    font-weight: bold;
  }
}
</style>
