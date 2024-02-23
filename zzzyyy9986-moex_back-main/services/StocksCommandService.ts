import {mode} from "../env";
import {Mods} from "../enums/Mods";
import * as timers from "timers";
import {randomIntFromInterval} from "../utils";

export class StocksCommandService {
    public static getRateByKeyWord(ticker:string,keyWord:string){
        const util = require('util');
        const exec = util.promisify(require('child_process').exec);
        if(mode === Mods.DEV){
            return  "echo " + randomIntFromInterval(0,100)/100 * -1 * randomIntFromInterval(0,1)
        }
        else {
            return 'python /root/proton/sentiment.py  --ticker "'+ticker+'" --search_query "'+keyWord+'" --period "month"';
        }
    }
    public static getRateByTitle(title:string){
        if(mode === Mods.DEV){
            return  "echo " + randomIntFromInterval(0,100)/100 * -1 * randomIntFromInterval(0,1)
        }
        else {
            return `python /root/proton/sent_title.py --title "${title}"`;
        }
    }
    public static getRateByArticle() {
        let x = ''

    }

}