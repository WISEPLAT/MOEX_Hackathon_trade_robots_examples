<template>
	<div class="hello" ref="chartdiv" id="chartdiv"></div>
</template>

<script lang="ts">
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";

export default {
	name: "HelloWorld",
	props: {
		data: {},
	},
	mounted() {
		let root = am5.Root.new("chartdiv");

		root.setThemes([am5themes_Animated.new(root)]);

		let chart = root.container.children.push(
			am5xy.XYChart.new(root, {
				panX: true,
				panY: true,
				wheelX: "zoomX",
			}),
		);

		let yAxis = chart.yAxes.push(
			am5xy.ValueAxis.new(root, {
				renderer: am5xy.AxisRendererY.new(root, {}),
			}),
		);

		let xAxis = chart.xAxes.push(
			am5xy.DateAxis.new(root, {
				baseInterval: {
					timeUnit: "minute",
					count: "1",
				},
				renderer: am5xy.AxisRendererX.new(root, {
					minorGridEnabled: true,
				}),
				tooltip: am5.Tooltip.new(root, {}),
			}),
		);

		// Create series
		let series1 = chart.series.push(
			am5xy.LineSeries.new(root, {
				name: "Динамика доходности сделок",
				xAxis: xAxis,
				yAxis: yAxis,
				valueYField: "dyn_trades_profit",
				valueXField: "Date",
			}),
		);
		series1.data.setAll(this.data);

		let series2 = chart.series.push(
			am5xy.LineSeries.new(root, {
				name: "Динамика доходности портфеля",
				xAxis: xAxis,
				yAxis: yAxis,
				valueXField: "Date",
				valueYField: "dyn_portfel_profit",
			}),
		);
		series2.data.setAll(this.data);

		let scrollbarX = am5xy.XYChartScrollbar.new(root, {
			orientation: "horizontal",
			height: 40,
		});

		chart.set("scrollbarX", scrollbarX);

		chart.set(
			"cursor",
			am5xy.XYCursor.new(root, {
				behavior: "zoomX",
			}),
		);

		// Add legend
		let legend = chart.children.push(am5.Legend.new(root, {}));
		legend.data.setAll(chart.series.values);

		// Add cursor
		chart.set("cursor", am5xy.XYCursor.new(root, {}));

		this.root = root;
	},

	beforeDestroy() {
		if (this.root) {
			this.root.dispose();
		}
	},
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.hello {
	width: 100%;
	height: 500px;
}
</style>
