<script setup lang="ts">
import { serviceFilename, statuses } from "~/types";
import type { BackTestResult } from "~/types/backTestResult";

import { useTasksStore } from "~/stores/tasksStore";
import CloseTaskButton from "~/components/utils/CloseTaskButton.vue";
const tasksStore = useTasksStore();

const tests = computed(() =>
	tasksStore.getTasksByService(serviceFilename.BACK_TESTING),
);

const taskResult = ref<BackTestResult>({ task_id: null });

const getRes = async (taskId) => {
	taskResult.value = await tasksStore.getTaskResult(taskId);
};

function isBuyHoldSharp(obj: any) {
	return (
		obj &&
		typeof obj.description === "string" &&
		typeof obj.value === "number"
	);
}
</script>

<template>
	<p v-if="tests.length === 0">Пока тестов нет!</p>
	<div v-else class="flex gap-7 flex-wrap">
		<div
			class="card hover:border-b-red-400 transition-all flex gap-6 flex-col p-4 border-2 rounded-xl"
			v-for="test in tests"
		>
			<div class="flex gap-4">
				<div class="border-r-2 pr-4 gap-3 flex flex-col">
					<CardHeading
						:heading="test.config.ticker"
						icon="ui/ic_ticker"
					/>
					<CardHeading
						:heading="statuses[test.status].title"
						:icon="statuses[test.status].icon"
					/>
				</div>
				<div class="flex flex-col gap-3">
					<CardHeading
						:heading="
							formatDate(test.config.start_date) +
							' - ' +
							formatDate(test.config.end_date)
						"
						icon="ui/ic_date"
						class="font-bold"
					/>
					<div class="flex gap-4">
						<div>
							<Tooltip :description="timeframes.description">
								<p class="font-bold">Таймфрейм</p>
								<p>{{ test.config.timeframe }}</p>
							</Tooltip>
						</div>
						<div>
							<Tooltip :description="maxBars.description">
								<p class="font-bold">Максимум неотмечено</p>
								<p>{{ test.config.max_unmark * 100 }} %</p>
							</Tooltip>
						</div>
						<div>
							<Tooltip :description="bars.description">
								<p class="font-bold">Период разметки</p>
								<p>{{ test.config.extr_bar_count }}</p>
							</Tooltip>
						</div>
					</div>
				</div>
			</div>
			<CloseTaskButton
				v-if="test.status !== 2 && test.status !== 3"
				:task-id="test.id"
			/>
			<div
				class="flex flex-col gap-4"
				v-if="test.status === 2"
				v-auto-animate
			>
				<button
					@click="getRes(test.id)"
					class="text-white"
					key="res_button"
				>
					Посмотреть результаты
				</button>
				<div
					v-if="taskResult.task_id"
					class="flex gap-4 items-center"
					key="dialogs"
				>
					<Dialog
						:ticker="test.config.ticker"
						description="dq"
						heading="Показатели"
						action="Показатели"
					>
						<div class="flex gap-4 flex-wrap">
							<template
								v-for="(value, key) in taskResult"
								:key="key"
							>
								<div
									class="w-fit border-b-2 p-2"
									v-if="isBuyHoldSharp(value)"
								>
									<p class="opacity-70">
										{{ value.description }}
									</p>
									<p class="font-bold">{{ value.value }}</p>
								</div>
							</template>
						</div>
					</Dialog>
					<Dialog action="Графики">
						<ClientOnly>
							<Tabs
								as="div"
								first-tab-title="Идеальная торговля"
								second-tab-title="Нейронная торговля"
							>
								<template #tab1>
									<XYChart
										:data="
											tasksStore.transformBackTestData(
												taskResult.dyn_neural_trading
													.value,
											)
										"
										:ticker="'fwef'"
										:timeframe="''"
									/>
								</template>

								<template #tab2>
									<XYChart
										:data="
											tasksStore.transformBackTestData(
												taskResult.dyn_ideal_trading
													.value,
											)
										"
										:ticker="'fwef'"
										:timeframe="''"
									/>
								</template>
							</Tabs>
						</ClientOnly>
					</Dialog>
				</div>
			</div>
		</div>
	</div>
</template>

<style scoped></style>
