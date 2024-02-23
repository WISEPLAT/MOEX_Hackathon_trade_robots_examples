<script setup lang="ts"></script>

<template>
	<div class="flex gap-4 flex-wrap">
		<table>
			<thead>
				<tr>
					<th>Datetime</th>
					<th>Markup Signals</th>
					<th>Neural Signals</th>
					<th>Neural Trends</th>
					<!-- Add more headers as needed -->
				</tr>
			</thead>
			<tbody>
				<tr
					v-for="(datetime, index) in taskResult.dyn_neural_trading
						.value.Datetime"
					:key="index"
				>
					<td>{{ datetime }}</td>
					<td>
						{{
							taskResult.singals_example.markup_signals.values[
								index
							]
						}}
					</td>
					<td>
						{{
							taskResult.singals_example.neural_signals.values[
								index
							]
						}}
					</td>
					<td>
						{{
							taskResult.singals_example.neural_trends.values[
								index
							]
						}}
					</td>
					<!-- Add more data cells as needed -->
				</tr>
			</tbody>
		</table>
	</div>
</template>

<style scoped></style>
