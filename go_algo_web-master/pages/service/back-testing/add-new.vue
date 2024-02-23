<script setup lang="ts">
import { serviceFilename } from "~/types";
import { useSecuritiesStore } from "~/stores/securitiesStore";
const securitiesStore = useSecuritiesStore();

const selectedTicker = useSelectedTickerStore();
const servicesStore = useServicesStore();
const tasksStore = useTasksStore();

const {
	selectedMarkUp,
	selectedBars,
	selectedMaxUnmarkedBars,
	selectedStartDate,
	selectedEndDate,
	selectedTimeframe,
	selectedNeuralNetwork,
	onSelect,
} = useSelectHandlers();

const neuralNetworks = computed(() =>
	tasksStore.getTasksByService(serviceFilename.NEURAL_LEARNING),
);
</script>

<template>
	<p v-if="neuralNetworks.length === 0" class="font-bold text-xl opacity-70">
		Пока сетей нет, эта страница бесполезна. Но вы можете почитать описания
		параметров!
	</p>
	<div class="flex flex-row flex-wrap gap-7 select-container">
		<SelectTicker
			title="Тикер"
			:items="securitiesStore.securities"
			:description="tickers.description"
			:is-full-sized="true"
			display-full-size-key="secname"
			display-key="secid"
		/>
		<Select
			title="Параметр разметки"
			:items="markupParameters.list"
			@select="(selected) => onSelect('selectedMarkUp', selected)"
			:description="markupParameters.description"
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
			title="Количество баров"
			units="шт."
			@select="(selected) => onSelect('selectedBars', selected)"
			:items="bars.list"
			:description="bars.description"
			display-key="value"
		/>
		<Select
			title="Максимум неразмеченных баров волны"
			:items="maxBars.list"
			@select="
				(selected) => onSelect('selectedMaxUnmarkedBars', selected)
			"
			:description="maxBars.description"
			units="%"
			display-key="value"
		/>
		<Select
			v-if="neuralNetworks.length !== 0"
			title="Какую сеть тестируем"
			description="Здесь можно выбрать сеть для тестирования. Выбрать можно только сеть, которая уже обучена."
			:items="neuralNetworks.filter((neural) => neural.status === 2)"
			@select="(selected) => onSelect('selectedNeuralNetwork', selected)"
			display-key="id"
		/>

		<Input
			type="date"
			@input="(selected) => onSelect('selectedStartDate', selected)"
			title="Тестовые данные с"
			id="start_date"
		/>
		<Input
			type="date"
			@input="(selected) => onSelect('selectedEndDate', selected)"
			title="Тестовые данные по"
			id="end_date"
		/>
	</div>
	<button
		class="text-white"
		:disabled="
			!selectedStartDate ||
			!selectedEndDate ||
			!selectedTicker.ticker.secid ||
			neuralNetworks.length === 0
		"
		@click="
			servicesStore.createBackTestTask({
				scaler_path: selectedNeuralNetwork.config.scaler_path,
				neural_path: selectedNeuralNetwork.config.neural_path,
				ticker: selectedTicker.ticker.secid,
				timeframe: selectedTimeframe.timeframe,
				start_date: selectedStartDate,
				end_date: selectedEndDate,
				count_points: selectedMarkUp.value,
				extr_bar_count: selectedBars.value,
				max_unmark: selectedMaxUnmarkedBars.value / 100.0,
			})
		"
	>
		Провести бэк-тест
	</button>
</template>

<style scoped></style>
