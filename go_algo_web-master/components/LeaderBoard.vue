<script setup lang="ts">
const securitiesStore = useSecuritiesStore();
</script>

<template>
	<div class="grid gap-4">
		<p class="text-2xl font-black">Высокий потенциал роста</p>
		<Tabs as="div" first-tab-title="Сегодня" second-tab-title="На 5 дней">
			<template #tab1>
				<div
					v-if="securitiesStore.dayLeaderboard.length !== 0"
					class="flex justify-between gap-4 flex-wrap cards"
				>
					<LeaderCard
						v-for="leader in securitiesStore.getDaySortedLeaderboard()"
						:leader="leader"
					/>
				</div>
				<div v-else class="opacity-70 font-bold">
					<p>Пока данных нет.</p>
				</div>
			</template>
			<template #tab2>
				<div
					v-if="securitiesStore.fiveDayLeaderboard.length !== 0"
					class="flex justify-between gap-4 flex-wrap cards"
				>
					<LeaderCard
						v-for="leader in securitiesStore.getFiveDaySortedLeaderboard()"
						:leader="leader"
					/>
				</div>
				<div v-else class="opacity-70 font-bold">
					<p>Пока данных нет.</p>
				</div>
			</template>
		</Tabs>
	</div>
</template>
<style scoped>
.cards {
	@media (max-width: 450px) {
		flex-wrap: nowrap;
		flex-direction: column;
	}
}
</style>
