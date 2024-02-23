export default function useSelectHandlers() {
	const state = reactive({
		selectedMarkUp: null,
		selectedTimeframe: null,
		selectedStartDate: null,
		selectedEndDate: null,
		selectedBars: null,
		selectedDatasetSize: null,
		selectedMaxUnmarkedBars: null,
		selectedEpochs: null,
		selectedStepsPerEpoch: null,
		selectedValidationSteps: null,
		selectedNewModelFlag: true,
		selectedLearningRate: null,
		selectedDataSet: null,
		selectedNeuralNetwork: null,
		selectedCountDays: null,
	});

	const onSelect = (key, selected) => {
		state[key] = selected;
		console.log(state[key]);
	};

	return {
		...toRefs(state),
		onSelect,
	};
}
