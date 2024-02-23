<script setup lang="ts">
const emit = defineEmits(["input"]);
const props = defineProps({
	type: {
		type: String,
		default: "text",
	},
	title: {
		type: String,
	},
	placeholder: {
		type: String,
		default: "Type something...",
	},
	id: {
		type: String,
	},
	description: String,
});

const value = ref("");

const handleInput = () => {
	emit("input", value.value);
};

onMounted(() => {
	handleInput();
});
</script>

<template>
	<div class="flex flex-col gap-3 border-2 rounded-2xl p-4">
		<label :for="id" class="text-2xl font-bold">{{ title }}</label>
		<p class="opacity-60">{{ description }}</p>
		<input
			v-model="value"
			@input="handleInput"
			:type="type"
			:placeholder="placeholder"
			:id="id"
			class="p-2 border-b-2 w-1/2 rounded-xl w-fit"
		/>
	</div>
</template>

<style scoped></style>
