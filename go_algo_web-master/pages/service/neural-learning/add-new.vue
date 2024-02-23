<script setup lang="ts">
import { serviceFilename } from "~/types";

const {
	selectedEpochs,
	selectedValidationSteps,
	selectedStepsPerEpoch,
	selectedTimeframe,
	selectedLearningRate,
	selectedNewModelFlag,
	selectedDataSet,
	onSelect,
} = useSelectHandlers();

const servicesStore = useServicesStore();
const tasksStore = useTasksStore();

const datasets = computed(() =>
	tasksStore.getTasksByService(serviceFilename.DATASET_GENERATION),
);
</script>

<template>
	<p v-if="datasets.length === 0" class="font-bold text-xl opacity-70">
		Пока датасетов нет, эта страница бесполезна. Но вы можете почитать
		описания параметров!
	</p>
	<div class="flex flex-row flex-wrap gap-7 select-container">
		<Select
			title="Число эпох"
			:items="epochs.list"
			:description="epochs.description"
			@select="(selected) => onSelect('selectedEpochs', selected)"
			units="шт."
			display-key="value"
		/>
		<Select
			title="Шаги за эпоху"
			:items="stepsPerEpoch.list"
			:description="stepsPerEpoch.description"
			@select="(selected) => onSelect('selectedStepsPerEpoch', selected)"
			units="шт."
			display-key="value"
		/>
		<Select
			title="Временная рамка"
			:items="timeframes.list"
			@select="(selected) => onSelect('selectedTimeframe', selected)"
			:description="timeframes.description"
			display-key="title"
		/>
		<Select
			title="Валидационные шаги"
			:items="validationSteps.list"
			:description="validationSteps.description"
			@select="
				(selected) => onSelect('selectedValidationSteps', selected)
			"
			units="шт."
			display-key="value"
		/>
		<Select
			v-if="datasets.length !== 0"
			title="Дата-сет"
			:items="datasets"
			description="Дата-сет для обучения."
			@select="(selected) => onSelect('selectedDataSet', selected)"
			display-key="id"
		/>
		<Input
			type="number"
			description="Скорость обучения сети. Например, 0.0001"
			@input="(selected) => onSelect('selectedLearningRate', selected)"
			title="Скорость обучения"
			id="learning_rate"
		/>
		<Input
			type="checkbox"
			v-model:checked="selectedNewModelFlag"
			description="Нажмите, если хотите обучить новую модель."
			@input="(selected) => onSelect('selectedNewModelFlag', selected)"
			title="Новая модель"
			id="new_model_flag"
		/>
	</div>
	<button
		class="text-white"
		:disabled="datasets.length === 0 || selectedLearningRate === ''"
		@click="
			servicesStore.createNeuralLearningTask({
				data_path: selectedDataSet.config.data_path,
				new_model_flag: !selectedNewModelFlag,
				learning_rate: selectedLearningRate,
				epochs: selectedEpochs.value,
				steps_per_epoch: selectedStepsPerEpoch.value,
				validation_steps: selectedValidationSteps.value,
			})
		"
	>
		Обучить сеть
	</button>
</template>

<style scoped></style>
