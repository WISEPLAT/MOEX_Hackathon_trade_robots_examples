<script setup>
const props = defineProps({
	dev: Object,
});
</script>

<template>
	<div class="dev-card grid grid-flow-col-dense gap-2">
		<img
			class="object-cover object-center rounded-2xl h-40"
			:src="dev.photo"
			alt=""
		/>
		<div class="w-fit flex flex-col gap-1">
			<p class="text-xl font-bold">{{ dev.name }}</p>
			<p class="opacity-50">{{ dev.role }}</p>
			<div>
				<p v-for="tag in dev.tags">{{ tag }}</p>
			</div>
			<p class="opacity-50">{{ dev.description }}</p>
		</div>
	</div>
</template>

<style scoped>
div {
	opacity: 1 !important;
}

img {
	min-width: 10em;
	min-height: 10em;
}

.dev-card {
	width: 45%;
}
</style>
