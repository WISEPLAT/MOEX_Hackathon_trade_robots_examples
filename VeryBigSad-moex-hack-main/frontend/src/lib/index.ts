// place files you want to import through the `$lib` alias in this folder.

import type { Data } from "plotly.js";

export type ShareInfo = {
    id: string;
    name: string;
    price: number;
    raising: boolean;
    sector: string;
    premium: boolean;
};

export type PricePeriod = { begin: Date; end: Date; price: number };
export type PricePlotData = { x: string[]; y: number[] };

function path(endpoint: string): string {
    return `https://khromdev.ru/api/v1/${endpoint}`;
}

export async function shares(): Promise<ShareInfo[]> {
    let data = await fetch(path("tickers/"), { method: "GET" });
    let json: any[] = await data.json();
    let res: ShareInfo[] = json.map(o => {
        let id: string = o.ticker;
        return {
            id,
            name: o.name,
            price: o.price,
            raising: o.is_positive_forecast,
            sector: o.sphere,
            premium: id.length == 5 && id.endsWith("P")
        };
    });
    return res;
}

export async function relevant_shares(
    id: string
): Promise<(ShareInfo & { correlation: number })[]> {
    let data = await fetch(path(`tickers/${id}/relevant/`), { method: "GET" });
    let json: any[] = await data.json();
    let res = json.map(o => {
        let id: string = o.ticker;
        return {
            correlation: o.correlation_score,
            ...json_to_share(id, o)
        };
    });
    return res;
}

function json_to_share(id: string, json: any): ShareInfo {
    return {
        id,
        name: json.name,
        price: json.price,
        raising: json.is_positive_forecast,
        sector: "Финансы", // TODO
        premium: id.length == 5 && id.endsWith("P")
    };
}

export async function price_history(id: string, timeline: TimelineOption): Promise<Data> {
    let offset: number;
    let period: string;
    switch (timeline) {
        case "day":
            offset = 1 * (24 * 60 * 60 * 1000);
            period = "1m";
            break;
        case "week":
            offset = 7 * (24 * 60 * 60 * 1000);
            period = "10m";
            break;
        case "month":
            offset = 30 * (24 * 60 * 60 * 1000);
            period = "1h";
            break;
        case "half-year":
            offset = 180 * (24 * 60 * 60 * 1000);
            period = "D";
            break;
        case "year":
            offset = 365 * (24 * 60 * 60 * 1000);
            period = "D";
            break;
        case "all-time":
            offset = 0; // TODO
            period = "D";
            break;
    }
    let date_end = new Date(Date.now()).toISOString().split("T")[0];
    let date_start = new Date(Date.now() - offset).toISOString().split("T")[0];

    const endpoint = `tickers/${id}/?date_start=${date_start}&date_end=${date_end}&period=${period}`;
    let fetched = await fetch(path(endpoint), { method: "GET" });
    let json: any[] = await fetched.json();
    let prices: PricePeriod[] = json.map(o => ({
        begin: new Date(o.begin),
        end: new Date(o.end),
        price: o.close
    }));
    let data: Data & { x: string[]; y: number[] } = {
        x: [],
        y: [],
        line: { color: "#FFF9F9" },
        hoverinfo: "none"
    };
    for (const price_period of prices) {
        data.x.push(price_period.begin.toUTCString());
        data.y.push(price_period.price);
    }
    return data;
}

export type TimelineOption = "day" | "week" | "month" | "half-year" | "year" | "all-time";
export const Timelines: { id: TimelineOption; name: string }[] = [
    { id: "day", name: "День" },
    { id: "week", name: "Неделя" },
    { id: "month", name: "Месяц" },
    { id: "half-year", name: "6 месяцев" },
    { id: "year", name: "Год" },
    { id: "all-time", name: "Всё время" }
];

export type File = { name: string; content: string };
