<script lang="ts">
    import type { ShareInfo } from "$lib";
    import PortfolioButton from "$lib/PortfolioButton.svelte";
    import { createEventDispatcher } from "svelte";

    export let share: ShareInfo;
    export let is_selected: boolean = false;
    export let icon: "show" | "hide" = "show";
    export let prefix: string | undefined = undefined;

    let dispatch = createEventDispatcher<{
        click_element: undefined;
    }>();
</script>

<button class="share" class:selected={is_selected} on:click={() => dispatch("click_element")}>
    <div>
        {#if prefix}
            <div class="prefix">{prefix}</div>
        {/if}
        {#if icon == "show"}
            <img src={`/companies/${share.id}.png`} alt="" />
        {/if}
        <div class="col1">
            <h2>{share.name}</h2>
            <h3>
                {#if share.premium}
                    <img class="premium" src="/icons/premium.svg" alt="premium" />
                {/if}
                {share.id}
            </h3>
        </div>
        <div class="col2">
            <span class="big-text">{share.price} ₽</span>
            <span class="trend">
                {#if share.raising}
                    <span class="raising">Будет расти</span>
                    <img src="/icons/trend_up.svg" alt="" />
                {:else}
                    <span>Будет падать</span>
                    <img src="/icons/trend_down.svg" alt="" />
                {/if}
            </span>
        </div>
        <PortfolioButton {share} />
    </div>
    <hr />
</button>

<style lang="scss">
    .share {
        display: flex;
        flex-direction: column;
        align-items: stretch;
        background-color: transparent;

        > div {
            display: flex;
            justify-content: stretch;
            align-items: center;
            gap: 12px;
            color: var(--text);

            > .prefix {
                font-size: 20px;
                line-height: 24px;
                margin-right: 4px;
            }
            > img {
                width: 24px;
                height: 24px;
                border-radius: 4px;
            }
            > .col1 {
                flex: 1;
                display: flex;
                flex-direction: column;
                align-items: start;
                gap: 4px;
                > h2 {
                    flex: 1;
                    font-size: 20px;
                    text-align: start;
                    word-break: break-all;
                }
                > h3 {
                    display: flex;
                    gap: 4px;
                    font-size: 14px;
                    line-height: 16px;
                }
            }
            > .col2 {
                flex: 0 1 content;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: end;

                > .trend {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    > img {
                        width: 16px;
                        height: 16px;
                    }
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
        > hr {
            width: 100%;
            height: 1px;
            border: 0;
            background-color: var(--text-disabled);
            margin-top: 7px;
        }
        &:hover > hr,
        &.selected > hr {
            height: 2px;
            background-color: var(--text);
            margin-top: 6px;
        }
    }
</style>
