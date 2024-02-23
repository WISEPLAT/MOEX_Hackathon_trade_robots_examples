<script lang="ts">
    import type { PageServerData } from "./$types";

    export let data: PageServerData;
</script>

<article>
    {#if data.headers && data.article}
        <section class="header">
            <h1>Источник</h1>
            <a href={data.article.source.href}>{data.article.source.name}</a>
        </section>
        <section class="main">
            <section class="table">
                <h1>Содержание</h1>
                {#each data.headers as header}
                    <a href={`#header-${header.content}`}>{header.content}</a>
                {/each}
            </section>
            <section class="content">
                <h1>{data.article.title}</h1>
                {#each data.article.content as entry}
                    {#if entry.kind == "header"}
                        <h2 id={`header-${entry.content}`}>{entry.content}</h2>
                    {:else if entry.kind == "paragraph"}
                        <p>{entry.content}</p>
                    {:else if entry.kind == "image"}
                        <img src={entry.src} alt="" />
                    {:else if entry.kind == "code"}
                        <pre>{entry.content}</pre>
                    {/if}
                {/each}
            </section>
        </section>
    {:else}
        <div class="404">404</div>
    {/if}
</article>

<style lang="scss">
    article {
        flex: 1;
        background-color: var(--block-background);
        border-radius: 12px;
        display: flex;
        padding: 32px 40px;
        padding-left: 0;
        overflow-y: hidden;
        > section {
            display: flex;
            flex-direction: column;
            &.header {
                flex: 0 0 200px;
                border-right: 1px solid #57595e;
                margin-right: 8px;

                > * {
                    align-self: center;
                }
            }
            &.main {
                flex: 1 0 0;
                overflow-y: scroll;
                > * {
                    max-width: 800px;
                }
                > .table {
                    display: flex;
                    flex-direction: column;
                    gap: 20px;
                    margin-bottom: 20px;
                }
                > .content {
                    display: flex;
                    flex-direction: column;
                    gap: 20px;
                    > pre {
                        display: block;
                        color: var(--text);
                    }
                }
            }
        }
    }
    h1 {
        font-size: 32px;
        line-height: 40px;
    }
</style>
