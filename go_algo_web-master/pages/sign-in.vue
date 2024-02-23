<script setup lang="ts"></script>

<template>
	<h1 class="text-6xl font-black">Вход</h1>
	<Input title="Логин" placeholder="Ваш логин" id="login" type="text" />
	<Input
		title="Пароль"
		placeholder="Ваш пароль"
		id="password"
		type="password"
	/>
	<NuxtLink to="/sign-up">Еще нет аккаунта? Создайте!</NuxtLink>
</template>

<style scoped></style>
