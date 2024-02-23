<script setup lang="ts">
const tasksStore = useTasksStore();
const props = defineProps({
	taskId: Number,
});
</script>

<template>
	<button
		@click="tasksStore.closeTask(taskId)"
		class="bg-red-300 hover:bg-red-200 transition-all"
	>
		Отменить таск
	</button>
</template>

<style scoped></style>
