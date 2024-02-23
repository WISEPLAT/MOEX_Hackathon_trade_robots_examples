<script lang="ts">
    import type { Data, PlotlyHTMLElement } from "plotly.js";
    import { onMount } from "svelte";
    import { get, type Writable } from "svelte/store";

    export let data: Writable<Data[]>;

    export let hover: { x: string; y: string } | undefined = undefined;

    let plot: PlotlyHTMLElement;
    let graph: HTMLElement;

    onMount(async () => {
        const Plotly = await import("plotly.js-dist");
        plot = await Plotly.newPlot(
            graph,
            get(data),
            {
                margin: { t: 10, b: 10, l: 50, r: 20, pad: 20 },
                xaxis: { visible: false },
                yaxis: { fixedrange: true, showgrid: false, color: "#FFF9F9" },
                plot_bgcolor: "transparent",
                paper_bgcolor: "transparent",
                hovermode: "x unified"
            },
            {
                displayModeBar: false,
                scrollZoom: false,
                responsive: true,
                doubleClick: false,
                showTips: false
            }
        );
        plot.on("plotly_hover", e => {
            if (e.points.length == 0) return;
            hover = {
                x: e.points[0].x!.toString(),
                y: e.points[0].y!.toString()
            };
        });
        plot.on("plotly_unhover", e => {
            hover = undefined;
        });
        data.subscribe(dat => {
            // TODO: reset range (zoom) when data changes.
            plot.data.splice(0, plot.data.length, ...dat);
            Plotly.redraw(plot);
        });
    });
</script>

 <!-- TODO: button to reset range -->
<div class="plot" bind:this={graph} />

<style lang="scss">
    .plot {
        height: 200px;
    }
</style>
