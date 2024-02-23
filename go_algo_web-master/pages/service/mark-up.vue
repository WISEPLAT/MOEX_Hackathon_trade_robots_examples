<script setup lang="ts"></script>

<template>
	<div class="flex gap-4 items-center page-header">
		<PageHeading icon="ui/ic_markup" title="Разметка" />
		<NuxtLink to="/service/mark-up/all">Все разметки</NuxtLink>
		<NuxtLink to="/service/mark-up/add-new">Добавить новую</NuxtLink>
	</div>
	<NuxtPage />
</template>

<style scoped lang="scss">
a {
	padding: 12px;
	transition: 0.3s;
	border-radius: 42px;
	border: 1px solid #a4a4a4 !important;

	&:hover {
		background-color: rgba(0, 0, 0, 0.1);
	}
}
</style>
