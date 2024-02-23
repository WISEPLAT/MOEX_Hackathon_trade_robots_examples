<script lang="ts">
    export let background: string;
</script>

<div class="scroll" style:--target={"red"}>
    <div class="gradient" />
    <slot />
    <div class="gradient" />
</div>

<style lang="scss">
    .scroll {
        position: relative;
        scrollbar-color: var(--text) transparent;
        overflow-y: scroll;
        --origin: rgba(16, 20, 27, 0);
        > .gradient {
            position: absolute;
            left: 0px;
            right: 0px;
            height: 40px;
            z-index: 1;
            &:nth-of-type(1) {
                top: 0;
                background: linear-gradient(to top, var(--origin) 0%, var(--target) 100%);
            }
            &:nth-of-type(2) {
                bottom: 0;
                background: linear-gradient(to bottom, var(--origin) 0%, var(--target) 100%);
            }
        }
    }
</style>
