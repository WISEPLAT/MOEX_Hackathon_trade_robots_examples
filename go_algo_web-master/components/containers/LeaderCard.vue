<script setup lang="ts">
const props = defineProps({
	leader: Object,
});
</script>

<template>
	<div
		class="flex card w-fit flex-row gap-2 p-3 border-2 rounded-xl hover:border-b-red-400 transition-all"
	>
		<div>
			<CardHeading :heading="leader.ticker" icon="ui/ic_ticker" />
			<CardHeading
				:heading="leader.timeframe + ' день'"
				icon="ui/ic_timeframe"
			/>
		</div>
		<div>
			<p>{{ leader.predict_price.toFixed(3) }}</p>
			<p
				:class="
					leader.predict_profit < 0
						? 'text-red-400'
						: 'text-green-400'
				"
			>
				{{
					leader.predict_profit !== 0
						? (leader.predict_profit * 100).toFixed(3)
						: leader.predict_profit
				}}%
			</p>
		</div>
	</div>
</template>

<style scoped>
.card {
	@media (max-width: 450px) {
		width: -webkit-fill-available;
		gap: 3rem;
	}
}
</style>
