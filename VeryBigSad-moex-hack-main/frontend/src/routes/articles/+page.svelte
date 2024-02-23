<script lang="ts">
    import Loader from "$lib/Loader.svelte";
    import type { ArticleInfo } from "$lib/articles.server";
    import type { PageServerData } from "./$types";

    export let data: PageServerData;

    let articles: ArticleInfo[] = data.articles;
</script>

<main>
    {#await articles}
        <Loader/>
    {:then articles}
        {#each articles as article}
            <a href={`/articles/${article.id}`}>
                <h2>{article.title}</h2>
                <p class="description">{article.description}</p>
            </a>
        {/each}
    {/await}
</main>

<style lang="scss">
    main {
        flex: 1 0 0;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        grid-auto-rows: 300px;
        gap: 20px 20px;
        align-items: stretch;

        > a {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 32px 40px;
            gap: 20px;
            border-radius: 12px;
            text-decoration: none;
            background-color: var(--block-background);

            > p {
                text-overflow: ellipsis;
                overflow: hidden;
            }
        }

        padding-right: 24px;
        margin-right: -24px;
        scrollbar-color: var(--text) transparent;
        overflow-y: scroll;
    }
</style>
