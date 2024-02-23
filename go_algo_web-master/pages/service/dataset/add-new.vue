<script setup lang="ts">
const servicesStore = useServicesStore();

const {
	selectedTimeframe,
	selectedMarkUp,
	selectedEndDate,
	selectedStartDate,
	selectedBars,
	selectedDatasetSize,
	selectedMaxUnmarkedBars,
	onSelect,
} = useSelectHandlers();

const validateYears = computed(() => {
	if (selectedStartDate.value && selectedEndDate.value) {
		const startDate = new Date(selectedStartDate.value);
		const endDate = new Date(selectedEndDate.value);
		const diffYears = endDate.getFullYear() - startDate.getFullYear();
		return diffYears >= 5;
	}
	return false;
});
</script>

<template>
	<div class="flex flex-row flex-wrap gap-7 select-container">
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
			title="Размер дата-сета"
			:items="maxDatasetSize.list"
			@select="(selected) => onSelect('selectedDatasetSize', selected)"
			units="гб."
			:description="maxDatasetSize.description"
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

		<Input
			type="date"
			@input="(selected) => onSelect('selectedStartDate', selected)"
			title="Разметить с"
			description="Дата начала получаемых для анализа данных."
			id="start_date"
		/>
		<Input
			type="date"
			@input="(selected) => onSelect('selectedEndDate', selected)"
			title="Разметить по"
			description="Дата окончания получаемых для анализа данных"
			id="end_date"
		/>
	</div>
	<button
		class="text-white"
		:disabled="!validateYears"
		@click="
			servicesStore.createGenDatasetTask({
				timeframe: selectedTimeframe.timeframe,
				count_points: selectedMarkUp.value,
				start_date: selectedStartDate,
				end_date: selectedEndDate,
				extr_bar_count: selectedBars.value,
				max_unmark: selectedMaxUnmarkedBars.value / 100.0,
				size_df: selectedDatasetSize.value,
			})
		"
	>
		Сгенерировать дата-сет
	</button>
	<p v-if="!validateYears" class="font-bold text-xl opacity-70">
		Для лучшей работы рекомендуется промежуток более 5 лет.
	</p>
</template>

<style scoped></style>
