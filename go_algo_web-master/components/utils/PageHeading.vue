<script setup lang="ts">
const props = defineProps({
	title: String,
	icon: String,
});
</script>

<template>
	<div class="flex flex-row gap-3 items-center">
		<NuxtIcon :name="icon" :alt="title" />
		<p class="text-2xl font-bold">{{ title }}</p>
	</div>
</template>

<style scoped></style>
