<script setup lang="ts">
import { serviceFilename } from "~/types";
import { useTasksStore } from "~/stores/tasksStore";
import NeuralCard from "~/components/containers/NeuralCard.vue";
const tasksStore = useTasksStore();
const networks = computed(() =>
	tasksStore.getTasksByService(serviceFilename.NEURAL_LEARNING),
);
</script>

<template>
	<div v-if="networks.length === 0">
		<p>Пока сетей нет!</p>
	</div>
	<div v-else class="flex gap-7 flex-wrap">
		<NeuralCard
			v-for="network in networks"
			class="card hover:border-b-red-400 transition-all flex gap-4 flex-col p-4 border-2 rounded-xl"
			:network="network"
		/>
	</div>
</template>

<style scoped></style>
