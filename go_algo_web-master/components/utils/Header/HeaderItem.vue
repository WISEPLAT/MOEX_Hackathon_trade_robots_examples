<script setup lang="ts">
const props = defineProps({
	title: String,
	navigateTo: String,
});
</script>

<template>
	<NuxtLink class="general-link" :to="props.navigateTo">{{
		props.title
	}}</NuxtLink>
</template>

<style scoped>
a {
	transition: 0.3s;
	border-radius: 42px;

	border: 1px solid #d5d5d5 !important;
	padding: 12px;
}
.router-link-active {
	text-decoration: underline;
	background-color: rgba(0, 0, 0, 0.05) !important;
	opacity: 1;
	font-weight: 800;
}
</style>
