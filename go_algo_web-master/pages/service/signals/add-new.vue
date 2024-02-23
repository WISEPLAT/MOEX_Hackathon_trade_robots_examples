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
	selectedTimeframe,
	selectedNeuralNetwork,
	selectedCountDays,
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
		<MultipleSelectTicker
			title="Тикеры"
			:items="securitiesStore.securities"
			:description="tickers.description"
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
			title="Количество дней"
			:items="countDays.list"
			:description="countDays.description"
			@select="(selected) => onSelect('selectedCountDays', selected)"
			display-key="value"
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
			title="Сеть для генерации"
			v-if="neuralNetworks.length !== 0"
			description="Здесь можно выбрать сеть для генерации. Выбрать можно только сеть, которая уже обучена."
			:items="neuralNetworks.filter((neural) => neural.status === 2)"
			@select="(selected) => onSelect('selectedNeuralNetwork', selected)"
			display-key="id"
		/>
	</div>
	<button
		class="text-white"
		:disabled="!selectedTicker.ticker[0] || neuralNetworks.length === 0"
		@click="
			servicesStore.createSignalsTask({
				ticker: selectedTicker.mapTickers(selectedTicker.ticker),
				scaler_path: selectedNeuralNetwork.config.scaler_path,
				neural_path: selectedNeuralNetwork.config.neural_path,
				timeframe: selectedTimeframe.timeframe,
				count_points: selectedMarkUp.value,
				extr_bar_count: selectedBars.value,
				max_unmark: selectedMaxUnmarkedBars.value / 100.0,
				count_days: selectedCountDays.value,
			})
		"
	>
		Сгенерировать сигналы
	</button>
</template>

<style scoped></style>
