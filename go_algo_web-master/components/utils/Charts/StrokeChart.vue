<template>
	<div class="hello" ref="chartdiv" id="chartdiv"></div>
</template>

<script lang="ts">
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import * as am5stock from "@amcharts/amcharts5/stock";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";

export default {
	name: "HelloWorld",
	props: {
		data: {},
	},
	mounted() {
		let root = am5.Root.new("chartdiv");

		root.setThemes([am5themes_Animated.new(root)]);

		let stockChart = root.container.children.push(
			am5stock.StockChart.new(root, {}),
		);

		// Create main panel
		let mainPanel = stockChart.panels.push(
			am5stock.StockPanel.new(root, {
				wheelY: "zoomX",
				panX: true,
				panY: true,
			}),
		);

		let valueAxis = mainPanel.yAxes.push(
			am5xy.ValueAxis.new(root, {
				renderer: am5xy.AxisRendererY.new(root, {}),
			}),
		);

		let dateAxis = mainPanel.xAxes.push(
			am5xy.GaplessDateAxis.new(root, {
				baseInterval: {
					timeUnit: "day",
					count: 1,
				},
				renderer: am5xy.AxisRendererX.new(root, {}),
			}),
		);

		// Create series
		let valueSeries = mainPanel.series.push(
			am5xy.LineSeries.new(root, {
				name: "STCK",
				valueXField: "Date",
				valueYField: "Close",
				xAxis: dateAxis,
				yAxis: valueAxis,
				legendValueText: "{valueY}",
			}),
		);

		valueSeries.data.setAll(this.data);
		stockChart.set("stockSeries", valueSeries);

		let valueLegend = mainPanel.plotContainer.children.push(
			am5stock.StockLegend.new(root, {
				stockChart: stockChart,
			}),
		);
		valueLegend.data.setAll([valueSeries]);

		let volumePanel = stockChart.panels.push(
			am5stock.StockPanel.new(root, {
				wheelY: "zoomX",
				panX: true,
				panY: true,
				height: am5.percent(30),
			}),
		);

		let volumeValueAxis = volumePanel.yAxes.push(
			am5xy.ValueAxis.new(root, {
				numberFormat: "#.#a",
				renderer: am5xy.AxisRendererY.new(root, {}),
			}),
		);

		let volumeDateAxis = volumePanel.xAxes.push(
			am5xy.GaplessDateAxis.new(root, {
				baseInterval: {
					timeUnit: "day",
					count: 1,
				},
				renderer: am5xy.AxisRendererX.new(root, {}),
			}),
		);

		let volumeSeries = volumePanel.series.push(
			am5xy.ColumnSeries.new(root, {
				name: "STCK",
				valueXField: "Date",
				valueYField: "Volume",
				xAxis: volumeDateAxis,
				yAxis: volumeValueAxis,
				legendValueText: "{valueY}",
			}),
		);

		volumeSeries.data.setAll(this.data);
		stockChart.set("volumeSeries", volumeSeries);

		let volumeLegend = volumePanel.plotContainer.children.push(
			am5stock.StockLegend.new(root, {
				stockChart: stockChart,
			}),
		);
		volumeLegend.data.setAll([volumeSeries]);

		mainPanel.set(
			"cursor",
			am5xy.XYCursor.new(root, {
				yAxis: valueAxis,
				xAxis: dateAxis,
				snapToSeries: [valueSeries],
				snapToSeriesBy: "y!",
			}),
		);

		volumePanel.set(
			"cursor",
			am5xy.XYCursor.new(root, {
				yAxis: volumeValueAxis,
				xAxis: volumeDateAxis,
				snapToSeries: [volumeSeries],
				snapToSeriesBy: "y!",
			}),
		);

		let scrollbar = mainPanel.set(
			"scrollbarX",
			am5xy.XYChartScrollbar.new(root, {
				orientation: "horizontal",
				height: 50,
			}),
		);
		stockChart.toolsContainer.children.push(scrollbar);

		let sbDateAxis = scrollbar.chart.xAxes.push(
			am5xy.GaplessDateAxis.new(root, {
				baseInterval: {
					timeUnit: "day",
					count: 1,
				},
				renderer: am5xy.AxisRendererX.new(root, {}),
			}),
		);

		let sbValueAxis = scrollbar.chart.yAxes.push(
			am5xy.ValueAxis.new(root, {
				renderer: am5xy.AxisRendererY.new(root, {}),
			}),
		);

		let sbSeries = scrollbar.chart.series.push(
			am5xy.LineSeries.new(root, {
				valueYField: "Close",
				valueXField: "Date",
				xAxis: sbDateAxis,
				yAxis: sbValueAxis,
			}),
		);

		sbSeries.fills.template.setAll({
			visible: true,
			fillOpacity: 0.3,
		});

		sbSeries.data.setAll(this.data);

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
