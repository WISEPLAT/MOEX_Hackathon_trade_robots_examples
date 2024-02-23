<script setup lang="ts">
const props = defineProps({
	heading: String,
	icon: String,
});
</script>

<template>
	<div class="flex flex-row opacity-70 items-center gap-2">
		<NuxtIcon :name="icon" :alt="heading" />
		<p>{{ heading }}</p>
	</div>
</template>

<style scoped></style>
