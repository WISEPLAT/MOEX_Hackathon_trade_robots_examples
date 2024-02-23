<script lang="ts">
    let show = false;
</script>

<button>
    i
    <div>
        <slot />
    </div>
</button>

<style lang="scss">
    button {
        width: 24px;
        height: 24px;
        position: relative;
        border-radius: 12px;
        color: var(--block-background);
        background-color: var(--text);

        > div {
            display: none;
        }
        &:hover > div, &:focus > div, div:hover {
            display: flex;
            flex-direction: column;
            position: absolute;
            border: 1px solid var(--text);
            border-radius: 12px;

            width: 380px;
            height: fit-content;
            color: var(--text);
            background-color: var(--block-background);
            top: 24px;
            margin-top: 2px;
        }
    }
</style>
