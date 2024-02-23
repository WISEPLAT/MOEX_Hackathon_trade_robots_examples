<script setup lang="ts">
const props = defineProps({
	description: String,
});

let showTooltip = ref(false);
</script>

<template>
	<div
		class="tooltip"
		v-auto-animate
		@mouseenter="showTooltip = true"
		@mouseleave="showTooltip = false"
	>
		<slot />
		<span
			v-if="showTooltip"
			:key="description"
			class="tooltip-content w-60 mt-14 self-center shadow-2xl"
			>{{ description }}</span
		>
	</div>
</template>

<style scoped>
/* Tooltip container */
.tooltip {
	position: relative;
	display: inline-flex;
	flex-direction: column;
	border-bottom: 1px dotted black; /* If you want dots under the hoverable text */
}

/* Tooltip text */
.tooltip .tooltip-content {
	background-color: #383838;
	color: #fff;
	text-align: center;
	padding: 0.5rem;
	border-radius: 6px;

	/* Position the tooltip text - see examples below! */
	position: absolute;
	z-index: 10;
}
</style>
