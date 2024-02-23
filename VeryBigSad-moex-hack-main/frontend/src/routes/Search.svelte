<script lang="ts">
    export let value: string;
    export let placeholder: string;
</script>

<input
    type="search"
    {placeholder}
    autocomplete="off"
    spellcheck="false"
    bind:value
    on:input
    on:change
    on:focus
    on:blur
    on:keydown
/>

<style lang="scss">
    input {
        width: 240px;
        height: 40px;

        border: 1px solid #555;
        padding: 12px 20px;
        padding-left: calc(12px + 18px + 12px);

        background: #3D3F42 url("/icons/search.svg") no-repeat 18px center;
        background-size: 18px;

        border: 0;
        border-radius: 12px;
        color: var(--text);

        &::placeholder {
            color: var(--text);
            font-size: 15px;
            opacity: 1;
        }
        &:focus {
            border-color: #1b1c1d;
            outline: none;
        }
    }
</style>
