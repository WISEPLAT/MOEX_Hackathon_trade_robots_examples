<script setup lang="ts">
import { serviceFilename, statuses } from "~/types";
import { useTasksStore } from "~/stores/tasksStore";
import CloseTaskButton from "~/components/utils/CloseTaskButton.vue";
const tasksStore = useTasksStore();
const datasets = computed(() =>
	tasksStore.getTasksByService(serviceFilename.DATASET_GENERATION),
);
</script>

<template>
	<div v-if="datasets.length === 0">
		<p>Пока датасетов нет!</p>
	</div>
	<div v-else class="flex gap-7 flex-wrap">
		<div
			v-for="dataset in datasets"
			class="card hover:border-b-red-400 transition-all flex gap-4 flex-col p-4 border-2 rounded-xl"
		>
			<div class="flex gap-4">
				<div class="border-r-2 pr-4 gap-3 flex flex-col">
					<CardHeading
						:heading="'Датасет ' + dataset.id"
						icon="ui/ic_dataset"
					/>
					<CardHeading
						:heading="statuses[dataset.status].title"
						:icon="statuses[dataset.status].icon"
					/>
				</div>
				<div class="flex flex-col gap-3">
					<CardHeading
						:heading="
							formatDate(dataset.config.start_date) +
							' - ' +
							formatDate(dataset.config.end_date)
						"
						icon="ui/ic_date"
						class="font-bold"
					/>
					<div class="flex gap-4">
						<div>
							<Tooltip :description="timeframes.description">
								<p class="font-bold">Таймфрейм</p>
								<p>{{ dataset.config.timeframe }}</p>
							</Tooltip>
						</div>
						<div>
							<Tooltip :description="maxBars.description">
								<p class="font-bold">Максимум неотмечено</p>
								<p>{{ dataset.config.max_unmark * 100 }} %</p>
							</Tooltip>
						</div>
						<div>
							<Tooltip :description="bars.description">
								<p class="font-bold">Период разметки</p>
								<p>{{ dataset.config.extr_bar_count }}</p>
							</Tooltip>
						</div>
					</div>
				</div>
			</div>
			<CloseTaskButton
				v-if="dataset.status !== 2 && dataset.status !== 3"
				:task-id="dataset.id"
			/>
		</div>
	</div>
</template>

<style scoped></style>
