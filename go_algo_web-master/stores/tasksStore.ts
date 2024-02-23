export const useTasksStore = defineStore("tasks", () => {
	const runtimeConfig = useRuntimeConfig();

	const tasks = ref([]);

	async function getAllTasks() {
		const { data: allTasks } = await useFetch(
			runtimeConfig.public.apiRoot + "task/lists/all",
		);

		tasks.value = allTasks.value;
	}

	function getTasksByService(service: string) {
		if (tasks.value) {
			return tasks.value.filter(
				(task) => task.config?.service === service,
			);
		}
	}

	async function closeTask(taskId: number) {
		const { data: closeTaskResult } = await useFetch(
			runtimeConfig.public.apiRoot + "task/close",
			{
				params: {
					task_id: taskId,
				},
			},
		);

		console.log(closeTaskResult.value);
		await getAllTasks();
	}

	async function getTaskResult(taskId: number) {
		const { data: taskResult } = await useFetch(
			runtimeConfig.public.apiRoot + "task/result",
			{
				params: {
					task_id: taskId,
				},
			},
		);

		return taskResult.value;
	}

	function transformMarkUpChartData(taskResult: any) {
		let values = taskResult;
		return values.Datetime.map((time, i) => ({
			Date: time / 1000000,
			Open: values.Open[i],
			High: values.High[i],
			Low: values.Low[i],
			Close: values.Close[i],
			Volume: values.Volume[i],
			Trend: values.Trend[i],
			Signals: values.Singals[i],
		}));
	}

	function transformBackTestData(taskResult: any) {
		return taskResult.Datetime.map((time, i) => ({
			Date: time / 1000000,
			dyn_trades_profit: taskResult.dyn_trades_profit[i],
			dyn_portfel_profit: taskResult.dyn_portfel_profit[i],
		}));
	}

	return {
		tasks,
		getAllTasks,
		getTasksByService,
		getTaskResult,
		closeTask,
		transformMarkUpChartData,
		transformBackTestData,
	};
});
