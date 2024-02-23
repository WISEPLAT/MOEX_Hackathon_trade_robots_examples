import axios, { AxiosResponse } from "axios";
import { CandleInterface } from "interfaces/candle.interface";


export async function getCandles(ticker: string, time: string, setCandles: (e: any) => void) {
    const { data: response }: AxiosResponse<CandleInterface[]> = await axios.get(process.env.NEXT_PUBLIC_DOMAIN +
       '/candles/name_ticker=' + ticker + '&date=2020-01-01&till_date=2020-12-31&period=' + time);

    setCandles(response);
}

export async function getNowPrice(ticker: string, setNowPrice: (e: any) => void) {
    let date = new Date();
    let year = date.getFullYear();
    let month = '' + date.getMonth() + 1;
    let day = '' + date.getDate();
    let lastDay = date.getDate() - 2 + '';

    month.length < 2 ? month = '0' + month : month = month;
    day.length < 2 ? day = '0' + day : day = day;
    lastDay.length < 2 ? lastDay = '0' + lastDay : lastDay = lastDay;
    
    const { data: response }: AxiosResponse<CandleInterface[]> = await axios.get(process.env.NEXT_PUBLIC_DOMAIN +
       '/candles/name_ticker=' + ticker + '&date=2023-12-01&till_date=2023-12-03&period=h');

    setNowPrice(response[response.length - 1].open);
}
