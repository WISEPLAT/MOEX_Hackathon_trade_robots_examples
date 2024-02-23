import * as express from "express";
import axios from "axios";
import {StocksCommandService} from "../services/StocksCommandService";
import {tickersKeyWords} from "../consts/tickers";
import {forEach} from "lodash";


//1) Новостная оценка
// python /root/proton/sentiment.py  --ticker "SBER" --search_query "Сбербанк | Сбер"
//1.1) Оценка по рынкам
// python /root/proton/get_price_change.py --ticker "SBER" --period "week"
//2)
//3) Оценка новости
// python /root/proton/sent_title.py --title "Сбер отчитался выше ожиданий рынка"


export class StocksController {
    // газпром|сбер|альфа|нефть
    public static async getNewsByTicker(req: express.Request, res: express.Response){
        console.log('тууууууут')
        const util = require('util');
        const exec = util.promisify(require('child_process').exec);
        let resp = []

        const ticker = req.body.ticker

        console.log(Object.keys(tickersKeyWords))


        const newsResp = await axios.get(`https://mediametrics.ru/satellites/api/search/?ac=search&nolimit=1&q=${tickersKeyWords[ticker]}&p=1&c=ru&d=month&sort=tm&dbg=debug&callback=JSON`)

         for(const item of newsResp.data.items) {
                console.log(item.title)
                const {stdout, stderr} = await exec(StocksCommandService.getRateByTitle(item.title))
                console.log(stdout)
                resp.push({
                    id: item.id,
                    title: item.title,
                    url: item.url,
                    value: +(stdout.replace("\n","") * 10),
                    source:item.url.split("/")[0],
                    time:item.timestamp,
                    ticker,
                })
        }
        res.send({
            data:resp
        })
    }
    public static async getStocksList(req: express.Request, res: express.Response){
        let  resp = []
        const util = require('util');
        const exec = util.promisify(require('child_process').exec);
        const tickers = req.body.tickers


        for (const ticker of tickers) {
            console.log('Иду по тикеру ' + ticker)
            const { stdout, stderr } = await exec(StocksCommandService.getRateByKeyWord(ticker,tickersKeyWords[ticker]));
            console.log('stout:'+stdout)
             resp.push({
                 ticker,
                 value:stdout
             })
        }
        await res.send({
            data:resp
        })
    }
}