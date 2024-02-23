<script lang="ts">
    import type { ShareInfo } from "$lib";
    import ShareView from "./ShareView.svelte";
    import SharesList from "./SharesList.svelte";
    import type { PageData } from "./$types";
    import { shares as get_shares } from "$lib";
    import { onMount } from "svelte";
    import Loader from "$lib/Loader.svelte";

    let shares: ShareInfo[] | undefined;
    let selected: ShareInfo | undefined = undefined;
    onMount(async () => {
        get_shares().then(s => (shares = s));
    });
</script>

<main>
    {#if !shares}
        <section class="empty loader">
            <Loader />
        </section>
    {:else}
        <SharesList {shares} bind:selected />
    {/if}
    {#if !selected}
        <section class="empty blur">
            <span>Выберите компанию<br/>из предложенного списка</span>
            <img src="/blur.svg" alt="" />
        </section>
    {:else}
        <ShareView share={selected} />
    {/if}
</main>

<style lang="scss">
    main {
        flex: 1;
        display: flex;
        gap: 20px;
        align-items: stretch;
        overflow-y: hidden;
        > .empty {
            flex: 1 0 0;
            padding: 32px 40px;
            border-radius: 12px;
            background-color: var(--block-background);
            overflow-y: hidden;
            &.loader {
                display: flex;
                align-items: center;
                justify-content: center;
            }
            &.blur {
                display: flex;
                justify-content: center;
                align-items: center;
                > span {
                    position: absolute;
                    text-align: center;
                    font-size: 20px;
                    line-height: 24px;
                }
                > img {
                    width: 100%;
                }
            }
        }
    }
</style>
