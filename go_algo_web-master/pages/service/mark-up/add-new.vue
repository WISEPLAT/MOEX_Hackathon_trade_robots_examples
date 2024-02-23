<script setup lang="ts">
import { useSecuritiesStore } from "~/stores/securitiesStore";

const securitiesStore = useSecuritiesStore();
const servicesStore = useServicesStore();
const selectedTicker = useSelectedTickerStore();

const {
	selectedMarkUp,
	selectedTimeframe,
	selectedStartDate,
	selectedEndDate,
	selectedBars,
	onSelect,
} = useSelectHandlers();
</script>

<template>
	<div class="select-container flex flex-row flex-wrap gap-7">
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
		<Input
			type="date"
			@input="(selected) => onSelect('selectedStartDate', selected)"
			title="Разметить с"
			id="start_date"
		/>
		<Input
			type="date"
			@input="(selected) => onSelect('selectedEndDate', selected)"
			title="Разметить по"
			id="end_date"
		/>
	</div>
	<button
		class="text-white"
		:disabled="
			!selectedStartDate ||
			!selectedEndDate ||
			!selectedTicker.ticker.secid
		"
		@click="
			servicesStore.createMarkUpTask({
				ticker: selectedTicker.ticker.secid,
				timeframe: selectedTimeframe.timeframe,
				count_points: selectedMarkUp.value,
				extr_bar_count: selectedBars.value,
				start_date: selectedStartDate,
				end_date: selectedEndDate,
			})
		"
	>
		Разметить
	</button>
</template>

<style scoped>
.select-container {
}
</style>
