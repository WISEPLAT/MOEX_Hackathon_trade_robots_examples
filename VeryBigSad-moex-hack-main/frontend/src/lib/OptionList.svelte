<script lang="ts" context="module">
    type Option = { name: string };
</script>

<script lang="ts" generics="T extends Option">
    export let options: T[];
    export let selected: T;
</script>

<menu>
    {#each options as option}
        <button class:selected={option == selected} on:click={() => selected = option}>
            {option.name}
        </button>
    {/each}
</menu>

<style lang="scss">
    menu {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        > button {
            color: var(--text);
            background-color: transparent;
            font-size: 14px;
            &.selected {
                font-weight: bold;
                color: var(--text);
            }
            &:not(.selected) {
                color: var(--text-secondary);
            }
            &:hover:not(.selected) {
                text-decoration: underline;
            }
        }
    }
</style>
