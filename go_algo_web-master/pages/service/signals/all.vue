<script setup lang="ts">
import { serviceFilename, statuses } from "~/types";
import { useTasksStore } from "~/stores/tasksStore";
import CloseTaskButton from "~/components/utils/CloseTaskButton.vue";
const tasksStore = useTasksStore();
const signals = computed(() =>
	tasksStore.getTasksByService(serviceFilename.SIGNALS),
);
</script>

<template>
	<div v-if="signals.length === 0">
		<p>Пока сигналов нет!</p>
	</div>
	<div v-else class="flex gap-7 flex-wrap">
		<div
			v-for="signal in signals"
			class="card hover:border-b-red-400 transition-all flex gap-4 flex-col p-4 border-2 rounded-xl"
		>
			<div class="flex gap-4">
				<div class="border-r-2 pr-4 gap-3 flex flex-col">
					<CardHeading
						:heading="'Сигнал ' + signal.id"
						icon="ui/ic_signals"
					/>
					<CardHeading
						:heading="statuses[signal.status].title"
						:icon="statuses[signal.status].icon"
					/>
				</div>
				<div class="flex flex-col gap-6">
					<div class="flex gap-4">
						<div>
							<Tooltip :description="timeframes.description">
								<p class="font-bold">Таймфрейм</p>
								<p>{{ signal.config.timeframe }}</p>
							</Tooltip>
						</div>
						<div>
							<Tooltip :description="maxBars.description">
								<p class="font-bold">Максимум неотмечено</p>
								<p>{{ signal.config.max_unmark * 100 }} %</p>
							</Tooltip>
						</div>
						<div>
							<Tooltip :description="bars.description">
								<p class="font-bold">Период разметки</p>
								<p>{{ signal.config.extr_bar_count }}</p>
							</Tooltip>
						</div>
					</div>
					<div class="flex gap-4">
						<div>
							<Tooltip :description="countDays.description">
								<p class="font-bold">Количество дней</p>
								<p>{{ signal.config.count_days }}</p>
							</Tooltip>
						</div>
						<div>
							<Tooltip
								:description="markupParameters.description"
							>
								<p class="font-bold">Параметр разметки</p>
								<p>{{ signal.config.count_points }}</p>
							</Tooltip>
						</div>
					</div>
				</div>
			</div>
			<CloseTaskButton
				v-if="signal.status !== 2 && signal.status !== 3"
				:task-id="signal.id"
			/>
		</div>
	</div>
</template>

<style scoped></style>
