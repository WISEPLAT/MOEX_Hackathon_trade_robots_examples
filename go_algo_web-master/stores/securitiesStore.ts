import { defineStore } from "pinia";
import type { Security } from "~/types";

export const useSecuritiesStore = defineStore("securities", () => {
	const runtimeConfig = useRuntimeConfig();
	const securities = ref<Security[]>([]);
	const dayLeaderboard = ref([]);
	const fiveDayLeaderboard = ref([]);

	const isSecuritiesFetched = ref(false);
	const isLeaderboardFetched = ref(false);
	async function fetchSecurities() {
		if (!isSecuritiesFetched.value) {
			const { data: securitiesData } = await useFetch(
				runtimeConfig.public.apiRoot + "data/lists/securities",
				{
					headers: {
						Authorization:
							"Basic dXNlcjpmODFiMWVmNC1hZjVlLTRlMDctODNjMy04ZTVhNzhiN2Y5ZjQ=",
					},
				},
			);

			securities.value = securitiesData.value;
			isSecuritiesFetched.value = true;
		}
	}

	async function fetchDayLeaderboard() {
		const { data: leaderboardData } = await useFetch(
			runtimeConfig.public.apiRoot + "leaderboard/byTimeFrame",
			{
				params: {
					tf: 1,
				},
			},
		);

		dayLeaderboard.value = leaderboardData.value;
	}

	async function fetchFiveDayLeaderboard() {
		const { data: leaderboardData } = await useFetch(
			runtimeConfig.public.apiRoot + "leaderboard/byTimeFrame",
			{
				params: {
					tf: 5,
				},
			},
		);

		fiveDayLeaderboard.value = leaderboardData.value;
	}

	function getDaySortedLeaderboard() {
		return dayLeaderboard.value
			.sort((a, b) => b.predict_profit - a.predict_profit)
			.slice(0, 7);
	}

	function getFiveDaySortedLeaderboard() {
		return fiveDayLeaderboard.value
			.sort((a, b) => b.predict_profit - a.predict_profit)
			.slice(0, 7);
	}

	return {
		securities,
		dayLeaderboard,
		fiveDayLeaderboard,
		isFetched: isSecuritiesFetched,
		isLeaderboardFetched,
		fetchSecurities,
		fetchDayLeaderboard,
		fetchFiveDayLeaderboard,
		getFiveDaySortedLeaderboard,
		getDaySortedLeaderboard,
	};
});
