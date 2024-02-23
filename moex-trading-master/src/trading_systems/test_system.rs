use std::env;

use chrono::{Datelike, NaiveDate};
use linked_hash_map::LinkedHashMap;
use teloxide::Bot;
use teloxide::prelude::{ChatId, Requester};
use tokio::runtime;

use crate::models::algopack::candle_trade_stats::CandleTradeStats;
use crate::traits::trade::Trade;

pub struct TestTradingSystem {
    financial_result: f64,
    bot: Bot,
    chanel_id: i64,
    months: LinkedHashMap<String, f64>,
    months_signals: LinkedHashMap<String, f64>,
}

impl Trade for TestTradingSystem {
    fn new() -> Self {
        Self {
            financial_result: 0.0,
            bot: Bot::from_env(),
            chanel_id: env::var("CHANEL_ID").expect("You need to specify the CHANEL_ID in the telegram").parse().unwrap(),
            months: LinkedHashMap::new(),
            months_signals: LinkedHashMap::new(),
        }
    }

    fn trade(&mut self, candle: CandleTradeStats) {
        if let Ok(date) = NaiveDate::parse_from_str(&*candle.tradedate, "%Y-%m-%d") {
            let year_month = format!("{}-{}", date.year(), date.month());

            match self.months.get(&*year_month) {
                None => { self.months.insert(year_month, candle.pr_high.unwrap_or_default()); }
                Some(price) => {
                    if price > &candle.pr_high.unwrap_or_default() {
                        self.months.insert(year_month, candle.pr_high.unwrap_or_default());
                    }
                }
            }
        }

        self.calculate_signal(candle);
    }
}

impl TestTradingSystem {

    fn send_message(&self, message: String) {
        runtime::Runtime::new().unwrap().block_on(async {
            self.bot
                .send_message(ChatId(self.chanel_id), message)
                .await
                .expect("Error by sending message");
        });
    }

    fn calculate_signal(&mut self, candle: CandleTradeStats) {
        let last_months_count = 3;
        if self.months.len() < last_months_count {
            return;
        }
        let max_price = self.months.iter().rev().take(last_months_count).map(|(_, &value)| value).fold(f64::NEG_INFINITY, f64::max);
        let current_price = candle.pr_low.unwrap();

        if current_price < max_price * 0.8 && candle.val.unwrap() > 10000000.0 {
            if let Ok(date) = NaiveDate::parse_from_str(&*candle.tradedate, "%Y-%m-%d") {
                let year_month = format!("{}-{}", date.year(), date.month());

                match self.months_signals.get(&*year_month) {
                    None => {
                        self.months_signals.insert(year_month, candle.pr_close.unwrap_or_default());
                        println!("Дата:{}, время: {}, покупка {} по {}", candle.tradedate, candle.tradetime, candle.secid, current_price);
                        self.send_message(format!("Дата:{}, время: {}, покупка {} по {}", candle.tradedate, candle.tradetime, candle.secid, current_price));
                    }
                    Some(_) => {}
                }
            }
        }
    }
    pub fn get_financial_result(&self) -> f64 {
        return self.financial_result;
    }
    pub fn get_months_result(&self) -> &LinkedHashMap<String, f64> {
        return &self.months;
    }
}