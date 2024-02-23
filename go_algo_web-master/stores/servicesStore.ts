import { serviceFilename } from "~/types";
import { SymbolKind } from "vscode-languageserver-types";
import Object = SymbolKind.Object;

export const useServicesStore = defineStore("services", () => {
	const runtimeConfig = useRuntimeConfig();

	const markUpResponse = ref({});
	const taskResponse = ref({});

	async function createTask(
		service: string,
		config: object,
		successfulMessage: string,
	) {
		const { data: taskResponse } = await useFetch(
			runtimeConfig.public.apiRoot + "task/add",
		);

		let dataGenConfig = config;
		if (service === serviceFilename.DATASET_GENERATION) {
			dataGenConfig.data_path = "app/data/" + taskResponse.value.id;
		}

		if (service === serviceFilename.NEURAL_LEARNING) {
			dataGenConfig.neural_path = "app/neurals/" + taskResponse.value.id;
			dataGenConfig.scaler_path = "app/scalers/" + taskResponse.value.id;
		}

		const { data: configResponse } = await useFetch(
			runtimeConfig.public.apiRoot + "conf/add",
			{
				method: "post",
				body: {
					service: service,
					...dataGenConfig,
					respos_url: "localhost:8080",
				},
			},
		);

		console.log("Created config: ", configResponse);

		console.log("Added task response: ", taskResponse);
		console.log("taskResponse id:", taskResponse.value.id);
		console.log("configResponse id:", configResponse.value.id);

		const { data: taskCreateResponse } = await useFetch(
			runtimeConfig.public.apiRoot + "task/setConfig",
			{
				method: "get",
				headers: {
					Authentication:
						"Basic cXdlcnR5QGdtaWFsLmNvbTpxd2VydHkxMjM=",
				},
				params: {
					task_id: taskResponse.value.id,
					conf_id: configResponse.value.id,
				},
			},
		);

		console.log("Set task config response:", taskCreateResponse);

		useNuxtApp().$toast.info(successfulMessage);
		await useTasksStore().getAllTasks();
	}

	async function createMarkUpTask(config: object) {
		await createTask(
			serviceFilename.MARK_UP,
			config,
			"Добавление разметки успешно!",
		);
	}

	async function createGenDatasetTask(config: object) {
		await createTask(
			serviceFilename.DATASET_GENERATION,
			config,
			"Добавление датасета успешно!",
		);
	}

	async function createNeuralLearningTask(config: object) {
		await createTask(
			serviceFilename.NEURAL_LEARNING,
			config,
			"Обучение нейросети началось!",
		);
	}

	async function createBackTestTask(config: object) {
		console.log(config);
		await createTask(
			serviceFilename.BACK_TESTING,
			config,
			"Тестирование нейросети началось!",
		);
	}
	async function createSignalsTask(config: object) {
		console.log(config);
		await createTask(
			serviceFilename.SIGNALS,
			config,
			"Генерация сигналов началась!",
		);
	}

	return {
		markUpResponse,
		taskResponse,
		createTask,
		createMarkUpTask,
		createGenDatasetTask,
		createNeuralLearningTask,
		createBackTestTask,
		createSignalsTask,
	};
});
