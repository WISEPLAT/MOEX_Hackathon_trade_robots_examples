<script setup lang="ts">
import MarkUpCard from "~/components/containers/MarkUpCard.vue";
import { serviceFilename } from "~/types";
import { useTasksStore } from "~/stores/tasksStore";
const tasksStore = useTasksStore();
const markups = computed(() =>
	tasksStore.getTasksByService(serviceFilename.MARK_UP),
);
</script>

<template>
	<div v-if="markups.length !== 0" class="flex gap-7 flex-wrap">
		<MarkUpCard v-for="markup in markups" :markup="markup" />
	</div>
	<div v-else>
		<p>Пока ничего нет</p>
	</div>
</template>

<style scoped></style>
