<script lang="ts" context="module">
    type Option = { id: string; label: string };
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<script lang="ts" generics="T extends Option">
    export let options: T[];
    export let value = options[0];

    let open = false;
    let focusOut = (e: FocusEvent) => {
        let target = e.relatedTarget;
        if (target && target instanceof HTMLElement && target.closest(".select")) return;
        open = false;
    };
</script>

<button class="select" on:click={() => (open = !open)} on:blur={focusOut}>
    <div class="header">
        <span>{value.label}</span>
        <img src={`/icons/arrow_drop_${open ? "up" : "down"}.svg`} alt="" />
    </div>
    <div class="options" class:open>
        {#each options as option}
            {#if option != value}
                <button on:click={() => (value = option)}>
                    {option.label}
                </button>
            {/if}
        {/each}
    </div>
</button>

<style lang="scss">
    .select {
        display: flex;
        gap: 4px;
        justify-content: space-between;
        position: relative;
        background-color: transparent;
        height: 16px;
        width: max-content;

        > .header {
            display: contents;
            &:hover > span {
                text-decoration: underline;
            }
        }

        > .options {
            display: none;
            position: absolute;
            top: 18px;
            left: -12px;
            padding: 8px 12px 12px 12px;
            width: max-content;
            min-width: 100%;
            border-radius: 0 0 12px 12px;
            background-color: var(--block-background);
            &.open {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }

            > button {
                color: var(--text);
                background-color: transparent;
                text-align: start;
                font-size: 14px;
                &:hover {
                    text-decoration: underline;
                }
            }
        }
    }
</style>
