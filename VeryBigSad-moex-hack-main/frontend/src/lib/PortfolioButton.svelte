<script lang="ts">
    import type { ShareInfo } from "$lib";
    import { portfolio } from "./Portfolio.svelte";

    export let share: ShareInfo;
</script>

<button on:click|stopPropagation={() => portfolio.toggle(share)}>
    {#if $portfolio.has(share.id)}
        <img src="/icons/done.svg" alt="Added" />
    {:else}
        <img src="/icons/plus.svg" alt="Add" />
    {/if}
</button>

<style lang="scss">
    button {
        width: 24px;
        height: 24px;
        background-color: transparent;
        > img {
            width: 24px;
            height: 24px;
        }
    }
</style>
