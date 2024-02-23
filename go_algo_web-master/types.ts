export type Security = {
	secid: string;
	shortname: string;
	secname: string;
};

export enum serviceFilename {
	MARK_UP = "data_markup.py",
	DATASET_GENERATION = "data_gen.py",
	BACK_TESTING = "calc_profit.py",
	SIGNALS = "calc_signals.py",
	NEURAL_LEARNING = "edu_neural.py",
}

export const statuses = {
	0: {
		icon: "ui/ic_in_queue",
		title: "В очереди",
	},
	1: {
		icon: "ui/ic_status_in_process",
		title: "В работе",
	},
	2: {
		icon: "ui/ic_selected",
		title: "Выполнен",
	},
	3: {
		icon: "ui/ic_with_error",
		title: "С ошибкой",
	},
};
