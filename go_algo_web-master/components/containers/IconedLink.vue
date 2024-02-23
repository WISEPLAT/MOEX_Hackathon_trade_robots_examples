<script setup lang="ts">
const props = defineProps({
	navigateTo: String,
	title: String,
});
</script>

<template>
	<a
		class="flex gap-3 w-fit hover:opacity-80 transition-all border-2 p-2 rounded-2xl opacity-40 items-center"
		:href="navigateTo"
		target="_blank"
	>
		<NuxtIcon class="opacity-70" name="ui/ic_link" alt="Link icon" />
		<p>{{ title }}</p>
	</a>
</template>

<style scoped></style>
