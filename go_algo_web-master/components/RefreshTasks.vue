<script setup lang="ts">
const tasksStore = useTasksStore();
const refreshTasks = async () => {
	await tasksStore.getAllTasks();
};

const props = defineProps({
	action: String,
});
</script>

<template>
	<button @click="refreshTasks">{{ action }}</button>
</template>

<style scoped></style>
