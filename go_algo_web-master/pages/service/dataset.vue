<script setup lang="ts"></script>

<template>
	<div class="flex gap-4 items-center page-header">
		<PageHeading icon="ui/ic_dataset" title="Дата-сеты" />
		<NuxtLink to="/service/dataset/all">Все дата-сеты</NuxtLink>
		<NuxtLink to="/service/dataset/add-new">Добавить новый</NuxtLink>
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
