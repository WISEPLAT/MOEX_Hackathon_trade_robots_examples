<script setup lang="ts">
const props = defineProps({
	profitWithoutShift: Object,
	profitWithShift: Object,
});
</script>

<template>
	<div>
		<div>
			<p>
				{{ profitWithoutShift.description }}
			</p>
			<p class="font-bold">
				{{ profitWithoutShift.value }}
			</p>
		</div>
		<div>
			<p>
				{{ profitWithShift.description }}
			</p>
			<p class="font-bold">
				{{ profitWithShift.value }}
			</p>
		</div>
	</div>
</template>

<style scoped></style>
