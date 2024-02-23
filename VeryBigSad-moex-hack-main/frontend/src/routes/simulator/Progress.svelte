<script lang="ts">
    export let percent: number = 50;
    $: style = `background: linear-gradient(to right, var(--good-color), var(--good-color) ${percent}%, var(--block-background) ${percent}%, var(--block-background));`;
</script>

<div {style}>
    {percent}%
</div>

<style lang="scss">
    div {
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        height: 24px;
        width: 120px;
        border: 1px solid var(--good-color);
        border-radius: 12px;
    }
</style>
