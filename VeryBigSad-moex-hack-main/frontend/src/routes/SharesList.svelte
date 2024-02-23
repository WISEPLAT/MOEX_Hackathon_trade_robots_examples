<script lang="ts">
    import type { ShareInfo } from "$lib";
    import InfoButton from "$lib/InfoButton.svelte";
    import OptionList from "$lib/OptionList.svelte";
    import Search from "./Search.svelte";
    import Share from "./Share.svelte";
    import Select from "$lib/Select.svelte";

    export let shares: ShareInfo[];
    export let selected: ShareInfo | undefined;

    /* Search */
    let search = "";
    $: search_filter = (s: ShareInfo) => {
        let _search = search.trim().toLowerCase();
        let _id = s.id.toLowerCase();
        let _name = s.name.toLowerCase();
        return _id.includes(_search) || _name.includes(_search);
    };
    /* Filtering */
    const filters = [
        { id: "all", name: "Все" },
        { id: "raising", name: "Только растущие" },
        { id: "falling", name: "Только убывающие" }
    ];
    let filter = filters[0];
    $: category_filter = (s: ShareInfo) => {
        if (filter.id == "all") {
            return true;
        } else if (filter.id == "raising") {
            return s.raising;
        } else if (filter.id == "falling") {
            return !s.raising;
        }
    };
    /* Sorting */
    const sorters = [
        { id: "alphabetic", label: "В алфавитном порядке" },
        { id: "expensive", label: "Сначала дорогие" },
        { id: "cheap", label: "Сначала дешёвые" }
    ];
    let sorter = sorters[0];
    let sorter_cmp: (a: ShareInfo, b: ShareInfo) => number;
    $: {
        if (sorter.id == "alphabetic") {
            sorter_cmp = (a, b) => {
                var nameA = a.name.toUpperCase();
                var nameB = b.name.toUpperCase();
                return nameA < nameB ? -1 : nameA > nameB ? 1 : 0;
            };
        } else if (sorter.id == "expensive") {
            sorter_cmp = (a, b) => b.price - a.price;
        } else if (sorter.id == "cheap") {
            sorter_cmp = (a, b) => a.price - b.price;
        }
    }
    $: filtered_shares = shares.filter(category_filter).filter(search_filter).sort(sorter_cmp);
</script>

<section>
    <header>
        <h2>Акции</h2>
        <InfoButton>
            <div style="padding: 20px; text-align: start;">
                <span>Данные взяты с </span><a href="https://www.moex.com/ru/algopack/">AlgoPack</a
                ><span
                    >. На данный момент на сайте представлена информация по 243 акциям, которые
                    торгуются на МосБирже</span
                >
            </div>
        </InfoButton>
    </header>
    <Search bind:value={search} placeholder="Найти акцию" />
    <div on:scroll={onscroll}>
        <menu>
            <OptionList options={filters} bind:selected={filter} />
            <Select options={sorters} bind:value={sorter} />
        </menu>
        {#each filtered_shares as share (share.id)}
            <Share
                {share}
                is_selected={share == selected}
                on:click_element={() => (selected = share)}
            />
        {/each}
    </div>
</section>

<style lang="scss">
    section {
        flex: 1;
        padding: 32px 40px;
        border-radius: 12px;
        background-color: var(--block-background);

        display: flex;
        flex-direction: column;
        > header {
            flex: 0 0 content;
            display: flex;
            justify-content: space-between;
            margin-bottom: 16px;
            > h2 {
                font-weight: bold;
                font-size: 20px;
            }
        }
        > div {
            flex: 1 0 0;
            display: flex;
            flex-direction: column;
            gap: 20px;
            overflow-y: scroll;

            padding-right: 16px;
            margin-right: -16px;
            scrollbar-color: var(--text) transparent;
            margin-top: 12px;

            > menu {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
        }
    }
</style>
