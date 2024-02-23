<script setup lang="ts"></script>

<template>
	<div class="flex gap-4 items-center page-header">
		<PageHeading icon="ui/ic_signals" title="Сигналы" />
		<NuxtLink to="/service/signals/all">Все сигналы</NuxtLink>
		<NuxtLink to="/service/signals/add-new">Добавить новую</NuxtLink>
	</div>
	<NuxtPage />
</template>

<style scoped>
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
