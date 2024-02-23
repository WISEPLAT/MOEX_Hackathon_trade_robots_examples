<script lang="ts">
    import type { File } from "$lib";

    export let files: File[];
    export let selected: File;
</script>

<menu>
    {#each files as file, i}
        <button on:click={() => (selected = file)} class:selected={selected == file}>
            <span>{file.name}</span>
            <button class="close" on:click={() => files.splice(i, 1)}>
                <img src="/icons/close.svg" alt="close" />
            </button>
        </button>
    {/each}
</menu>

<style lang="scss">
    menu {
        display: flex;
        width: min-content;
        > button {
            flex: 1 1 150px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 32px;
            border: 1px solid #56595e;
            gap: 8px;
            padding: 8px 16px;
            background-color: transparent;
            white-space: nowrap;
            text-overflow: ellipsis;

            &.selected {
                background-color: #3d3f42;
            }
            &:not(.selected) > .close {
                display: none;
            }
            > .close {
                background-color: transparent;
                padding: 2px;
                width: 20px;
                height: 20px;
                border-radius: 12px;
                > img {
                    width: 16px;
                    height: 16px;
                }
                &:hover {
                    background-color: rgba(255, 255, 255, 0.25);
                }
            }
        }
    }
</style>
