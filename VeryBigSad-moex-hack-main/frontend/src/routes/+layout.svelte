<script lang="ts">
    import { page } from "$app/stores";
    import Portfolio from "$lib/Portfolio.svelte";
    import "../app.scss";

    let entries = [
        { href: "/", title: "Главная" },
        { href: "/articles/guide", title: "Входим в алготрейдинг" },
        { href: "/simulator", title: "Протестировать свой алгоритм" },
        { href: "/articles", title: "Статьи" }
    ];

    $: current_page = $page.url.pathname;

    let show_portfolio = false;
</script>

<div id="wrapper">
    {#if show_portfolio}
        <Portfolio bind:show={show_portfolio} />
    {/if}
    <nav>
        <ul>
            {#each entries as entry}
                <a href={entry.href} class:current={current_page == entry.href}>{entry.title}</a>
            {/each}
        </ul>
        <button on:click={() => show_portfolio = !show_portfolio}>
            <img src="/icons/case.svg" alt="profile" />
        </button>
    </nav>
    <slot />
</div>

<style lang="scss">
    #wrapper {
        display: flex;
        flex-direction: column;
        align-items: stretch;
        gap: 20px;

        height: 100dvh;
        width: 100dvw;
        padding: 40px 50px;
        background-color: var(--page-background);

        > nav {
            flex: 0 0 64px;
            display: flex;
            gap: 20px;
            > ul {
                flex: 1;
                display: flex;
                justify-content: start;
                align-items: center;
                gap: 32px;
                padding: 20px 32px;
                border-radius: 12px;
                background-color: var(--block-background);
                > a {
                    font-size: 20px;
                    color: var(--text);
                    text-decoration: none;
                    text-align: center;
                    &.current {
                        font-weight: bold;
                    }
                }
            }
            > button {
                width: 64px;
                height: 64px;
                border-radius: 12px;
                background-color: var(--block-background);
                > img {
                    width: 24px;
                    height: 24px;
                    margin: 20px;
                }
            }
        }
    }
</style>
