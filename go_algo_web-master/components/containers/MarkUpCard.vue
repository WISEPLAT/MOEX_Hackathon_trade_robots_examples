<template>
	<div
		class="border-2 card hover:border-b-red-400 transition-all rounded-xl p-4 flex flex-col gap-4"
		v-auto-animate
	>
		<div class="flex gap-4">
			<div class="border-r-2 pr-4 gap-3 flex flex-col">
				<CardHeading
					:heading="markup.config.ticker"
					icon="ui/ic_ticker"
				/>
				<p class="font-bold text-xl">{{}}</p>
				<CardHeading
					:heading="statuses[markup.status].title"
					:icon="statuses[markup.status].icon"
				/>
			</div>
			<div class="flex flex-col gap-4">
				<CardHeading
					:heading="
						formatDate(markup.config.start_date) +
						' - ' +
						formatDate(markup.config.end_date)
					"
					icon="ui/ic_date"
					class="font-bold"
				/>
				<div class="flex flex-row gap-6">
					<div>
						<Tooltip :description="timeframes.description">
							<p class="font-bold">Таймфрейм</p>
							<p>{{ markup.config.timeframe }}</p>
						</Tooltip>
					</div>
					<div>
						<Tooltip :description="markupParameters.description">
							<p class="font-bold">Параметр разметки</p>
							<p>{{ markup.config.count_points }}</p>
						</Tooltip>
					</div>
					<div>
						<Tooltip :description="bars.description">
							<p class="font-bold">Количество баров</p>
							<p>{{ markup.config.extr_bar_count }}</p>
						</Tooltip>
					</div>
				</div>
			</div>
		</div>
		<CloseTaskButton
			v-if="markup.status !== 2 && markup.status !== 3"
			:task-id="markup.id"
		/>
		<button
			class="text-white hover:border-red-300 transition-all"
			:disabled="markup.status !== 2 || taskResult.profit_with_shift"
			@click="getRes"
		>
			Получить результаты
		</button>
		<div
			key="dialog"
			class="text-black"
			v-if="taskResult.profit_with_shift"
		>
			<Dialog
				heading="График"
				:ticker="markup.config.ticker"
				action="Показать график"
				description="gerrg"
			>
				<ClientOnly>
					<Chart
						:data="transformedChartData"
						:ticker="markup.config.ticker"
						:timeframe="timeframeMapping[markup.config.timeframe]"
					/>
					<ProfitCard
						:profit-without-shift="taskResult.profit_without_shift"
						:profit-with-shift="taskResult.profit_with_shift"
					/>
				</ClientOnly>
			</Dialog>
		</div>
	</div>
</template>
<script setup lang="ts">
import { statuses } from "~/types";
import { bars, timeframeMapping } from "~/utils/parameters";
import CloseTaskButton from "~/components/utils/CloseTaskButton.vue";

const tasksStore = useTasksStore();
const taskResult = ref({});
let transformedChartData = [];

const getRes = async () => {
	taskResult.value = await tasksStore.getTaskResult(props.markup.id);

	transformedChartData = tasksStore.transformMarkUpChartData(
		taskResult.value.markup.values,
	);
};

const props = defineProps({
	markup: Object,
});
</script>

<style scoped>
button {
	color: #fff;
}

.card {
	@media (max-width: 400px) {
		width: -webkit-fill-available;
	}
}
</style>
