import type { Security } from "~/types";

export const useSelectedTickerStore = defineStore({
	id: "selectedTicker",
	state: () => ({
		ticker: <Security>[],
	}),
	actions: {
		selectTicker(tickers) {
			this.ticker = tickers;
			console.log(this.ticker);
		},
		mapTickers(tickers) {
			return JSON.stringify(tickers.map((ticker) => ticker.secid));
		},
	},
});

export const useSelectedTimeframeStore = defineStore({
	id: "selectedTimeframe",
	state: () => ({
		timeframe: null,
	}),
	actions: {
		selectTicker(timeframe) {
			this.timeframe = timeframe;
		},
	},
});
