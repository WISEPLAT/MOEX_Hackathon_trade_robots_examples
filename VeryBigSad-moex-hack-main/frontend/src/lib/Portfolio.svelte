<script lang="ts" context="module">
    import type { ShareInfo } from "$lib";
    import { writable } from "svelte/store";

    let _store = writable(new Map<string, ShareInfo>());
    export const portfolio = {
        subscribe: _store.subscribe,
        toggle: (val: ShareInfo) => {
            _store.update(s => {
                if (s.has(val.id)) {
                    s.delete(val.id);
                } else {
                    s.set(val.id, val);
                }
                return s;
            });
        }
    };
</script>

<script lang="ts">
    import Share from "../routes/Share.svelte";
    import InfoButton from "./InfoButton.svelte";
    import { onMount } from "svelte";

    export let show: boolean;

    let dialog: HTMLDialogElement;
    let x = 0;
    let y = 0;
    onMount(() => {
        x = window.innerWidth / 2 - dialog.offsetWidth / 2;
        y = window.innerHeight / 2 - dialog.offsetHeight / 2;
    });
    let move = (e: MouseEvent) => {
        if (e.buttons % 2 != 1) return;
        x += e.movementX;
        y += e.movementY;

        let max_x = window.innerWidth - dialog.offsetWidth - 1;
        let max_y = window.innerHeight - dialog.offsetHeight - 3;
        if (x < 0) x = 0;
        else if (x > max_x) x = max_x;
        if (y < 0) y = 0;
        else if (y > max_y) y = max_y;
    };
</script>

<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
<dialog bind:this={dialog} style:left={x + "px"} style:top={y + "px"} on:mousemove={move}>
    <header>
        <InfoButton />
        <h2>Портфель</h2>
        <button on:click={() => (show = false)}>
            <img src="/icons/close.svg" alt="close" />
        </button>
    </header>
    <section>
        {#each $portfolio.values() as share}
            <Share {share} icon="hide" />
        {/each}
    </section>
</dialog>

<style lang="scss">
    dialog {
        display: flex;
        flex-direction: column;
        gap: 20px;
        position: absolute;
        width: 480px;
        z-index: 2;
        padding: 32px 40px;
        background-color: var(--block-background);
        border-radius: 12px;
        border: 1px solid var(--text);
        > header {
            display: flex;
            gap: 20px;
            > button {
                margin-left: auto;
                background-color: transparent;
            }
        }
        > section {
            display: flex;
            flex-direction: column;
            gap: 20px;
            height: 200px;
            overflow-y: scroll;
            padding-right: 20px;
            margin-right: -20px;
            scrollbar-color: var(--text) transparent;
        }
    }
</style>
