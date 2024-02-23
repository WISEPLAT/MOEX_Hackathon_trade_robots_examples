<script setup lang="ts">
const props = defineProps({
	strategy: Object,
});
</script>

<template>
	<div class="flex flex-col gap-4 p-4 select-none cursor-pointer">
		<h3>{{ strategy.title }}</h3>
		<CardHeading :heading="strategy.ticker" icon="ui/ic_ticker" />
		<CardHeading :heading="strategy.status" icon="ui/ic_status" />
	</div>
</template>

<style scoped lang="scss">
div:has(> h3) {
	border-radius: 20px;
	border: 1px solid #cdcdcd;
	opacity: 0.8;

	transition: 0.2s;
	&:hover {
		opacity: 1;
		transform: translateY(-5px);
		border: 1px solid #cc6b6b;
	}
}
</style>
