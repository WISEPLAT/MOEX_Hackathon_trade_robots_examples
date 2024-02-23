<script lang="ts">
    import { price_history, Timelines, type ShareInfo, relevant_shares } from "$lib";
    import InfoButton from "$lib/InfoButton.svelte";
    import OptionList from "$lib/OptionList.svelte";
    import { formatDate } from "$lib/util";
    import { onMount } from "svelte";
    import Share from "./Share.svelte";
    import PortfolioButton from "$lib/PortfolioButton.svelte";
    import { portfolio } from "$lib/Portfolio.svelte";
    import Plot from "$lib/Plot.svelte";
    import type { Data } from "plotly.js";
    import { writable } from "svelte/store";

    /* Timeline */
    let timeline = Timelines[1];
    /* Share */
    export let share: ShareInfo;
    let plot_data = writable(new Array<Data>());
    $: price_history(share.id, timeline.id).then(h => plot_data.set([h]));
    /* Hover */
    let hover: { x: string; y: string } | undefined = undefined;
    $: hover_price = hover ? hover.y : share.price;
    $: hover_date = hover ? new Date(hover.x) : new Date(2023, 1, 4);
    /* Correlations */
    const correlation_options = [
        { id: "high", name: "Высокая корреляция" },
        { id: "low", name: "Низкая корреляция" },
        { id: "portfolio", name: "Из портфеля" }
    ];
    let correlation_option = correlation_options[0];

    let _correlations = new Array<ShareInfo & { correlation: number }>();
    $: relevant_shares(share.id).then(s => (_correlations = s));
    $: correlations = _correlations
        .filter(s => correlation_option.id != "portfolio" || $portfolio.has(s.id))
        .sort((a, b) =>
            correlation_option.id == "low"
                ? a.correlation - b.correlation
                : b.correlation - a.correlation
        )
        .slice(0, 40);

    onMount(async () => {
        _correlations = await relevant_shares(share.id);
    });
</script>

<section class="share">
    <header>
        <img src={`/companies/${share.id}.png`} alt="" />
        <div class="name">
            <h2>{share.name}</h2>
            <span>
                {#if !share.premium}
                    {`${share.id} — Обычная акция`}
                {:else}
                    {`${share.id} — Привилегированная акция`}
                {/if}
            </span>
        </div>
        <PortfolioButton {share} />
    </header>
    <section class="attributes">
        <article class="sector">
            <span>Сектор</span>
            <span class="name">{share.sector}</span>
        </article>
        <article class="price">
            <span class="big-text">{share.price} ₽</span>
            <span class="trend">
                {#if share.raising}
                    <img src="/icons/trend_up.svg" alt="" />
                    <span class="raising">Будет расти</span>
                {:else}
                    <img src="/icons/trend_down.svg" alt="" />
                    <span>Будет падать</span>
                {/if}
            </span>
        </article>
    </section>
    <div class="scroll">
        <section class="graph">
            <OptionList options={Timelines} bind:selected={timeline} />
            <hr />
            <Plot data={plot_data} bind:hover />
            <hr />
            <div class="price">
                <span class="big-text">{hover_price} ₽</span>
                <span>{formatDate(hover_date)}</span>
            </div>
        </section>
        <section class="correlations">
            <header>
                <h3>Перечень корреляций</h3>
                <InfoButton></InfoButton>
            </header>
            <OptionList options={correlation_options} bind:selected={correlation_option} />
            <div class="correlations-list">
                {#each correlations as entry}
                    <Share share={entry} prefix={entry.correlation.toFixed(2)} />
                {/each}
            </div>
        </section>
    </div>
</section>

<style lang="scss">
    .share {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 20px;
        padding: 32px 40px;
        border-radius: 12px;
        background-color: var(--block-background);
        > header {
            display: flex;
            align-items: center;
            gap: 12px;
            > img {
                width: 44px;
                height: 44px;
            }
            > .name {
                display: flex;
                flex-direction: column;
                gap: 4px;
                margin-right: auto;
            }
        }
        > .attributes {
            display: flex;
            gap: 12px;
            > article {
                display: flex;
                flex-direction: column;
                padding: 8px 21px;
                border-radius: 12px;
                border: 1px solid var(--text-disabled);
            }
            > .sector {
                > .name {
                    font-size: 20px;
                    line-height: 24px;
                }
            }
            > .price {
                display: flex;
                justify-content: center;
                .trend {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    white-space: nowrap;
                    > span {
                        font-size: 14px;
                        &.raising {
                            color: var(--good-color);
                        }
                        &:not(.raising) {
                            color: var(--bad-color);
                        }
                    }
                }
            }
        }
        .scroll {
            flex: 1 0 0;
            overflow-y: scroll;
            padding-right: 16px;
            margin-right: -16px;

            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        .graph {
            display: flex;
            flex-direction: column;
            justify-content: stretch;
            align-items: stretch;
            > .price {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            > hr {
                width: 100%;
                height: 1px;
                border: 0;
                background-color: var(--text);
                margin: 8px 0;
            }
        }
        .correlations {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: stretch;
            > header {
                display: flex;
                justify-content: space-between;
                margin-bottom: 8px;
            }
            > .correlations-list {
                flex: 1 0 0;
                display: flex;
                flex-direction: column;
                gap: 20px;

                scrollbar-color: var(--text) transparent;
                margin-top: 16px;
            }
        }
    }
</style>
