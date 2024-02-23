<script setup lang="ts">
import { statuses } from "~/types";
import { useTasksStore } from "~/stores/tasksStore";

const props = defineProps({
	network: Object,
});

const tasksStore = useTasksStore();

const taskResult = ref({ task_id: null });

const getRes = async (taskId) => {
	taskResult.value = await tasksStore.getTaskResult(taskId);
};

function isBuyHoldSharp(obj: any) {
	return (
		obj &&
		typeof obj.description === "string" &&
		typeof obj.values === "number"
	);
}
</script>

<template>
	<div>
		<div class="flex gap-4">
			<div class="border-r-2 pr-4 gap-3 flex flex-col">
				<CardHeading
					:heading="'Сеть ' + network.id"
					icon="ui/ic_neural_network"
				/>
				<CardHeading
					:heading="statuses[network.status].title"
					:icon="statuses[network.status].icon"
				/>
			</div>
			<div class="flex flex-row gap-4">
				<div>
					<p class="font-bold">Скорость обучения</p>
					<p>{{ network.config.learning_rate }}</p>
				</div>
				<div>
					<Tooltip :description="epochs.description">
						<p class="font-bold">Эпохи</p>
						<p>{{ network.config.epochs }}</p>
					</Tooltip>
				</div>
				<div>
					<Tooltip :description="stepsPerEpoch.description">
						<p class="font-bold">Шаги за эпоху</p>
						<p>{{ network.config.steps_per_epoch }}</p>
					</Tooltip>
				</div>
			</div>
		</div>
		<div
			class="flex flex-col gap-4"
			v-if="network.status === 2"
			v-auto-animate
		>
			<button
				@click="getRes(network.id)"
				class="text-white"
				:disabled="taskResult.task_id"
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
					:ticker="network.id.toString()"
					description=""
					heading="Показатели модели "
					action="Показатели модели"
				>
					<Tabs
						as="div"
						first-tab-title="Loss"
						second-tab-title="Параметры"
					>
						<template #tab1>
							<table
								class="min-w-full divide-y divide-gray-200 rounded-lg shadow-sm overflow-hidden"
							>
								<thead
									class="bg-red-400 text-white font-medium"
								>
									<tr>
										<th
											class="px-6 py-3 text-left text-xs uppercase tracking-wider"
										>
											Index
										</th>
										<th
											class="px-6 py-3 text-left text-xs uppercase tracking-wider"
										>
											{{
												taskResult.edu_graph_losses.loss
													.description
											}}
										</th>
										<th
											class="px-6 py-3 text-left text-xs uppercase tracking-wider"
										>
											{{
												taskResult.edu_graph_losses
													.val_loss.description
											}}
										</th>
									</tr>
								</thead>
								<tbody
									class="bg-white divide-y divide-gray-200"
								>
									<tr
										v-for="(value, index) in taskResult
											.edu_graph_losses.loss.values"
										:key="index"
									>
										<td class="px-6 py-4 whitespace-nowrap">
											{{ index + 1 }}
										</td>
										<td class="px-6 py-4 whitespace-nowrap">
											{{ value }}
										</td>
										<td class="px-6 py-4 whitespace-nowrap">
											{{
												taskResult.edu_graph_losses
													.val_loss.values[index]
											}}
										</td>
									</tr>
								</tbody>
							</table>
						</template>
						<template #tab2>
							<div class="flex gap-4 flex-wrap">
								<template
									v-for="(value, key) in taskResult"
									:key="key"
								>
									<div
										v-if="isBuyHoldSharp(value)"
										class="w-fit border-b-2 p-2"
									>
										<p class="opacity-70">
											{{ value.description }}
										</p>
										<p class="font-bold">
											{{ value.values }}
										</p>
									</div>
								</template>
							</div>
						</template>
					</Tabs>
				</Dialog>
			</div>
		</div>
		<CloseTaskButton
			v-if="network.status !== 2 && network.status !== 3"
			:task-id="network.id"
		/>
	</div>
</template>

<style scoped></style>
