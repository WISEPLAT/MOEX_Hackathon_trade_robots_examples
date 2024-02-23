use crate::models::algopack::candle_trade_stats::CandleTradeStats;

pub trait Trade {
    fn new() -> Self;
    fn trade(&mut self, record: CandleTradeStats);
}