use std::fs::File;
use std::time::Instant;

use crate::models::algopack::candle_trade_stats::CandleTradeStats;
use crate::trading_systems::test_system::TestTradingSystem;
use crate::traits::trade::Trade;

pub fn test() {
    // let file_path = "algopack_data/tradestats_MOEX 1 short.csv";
    let file_path = "algopack_data/tradestats_MOEX 1.csv";
    // let file_path = "algopack_data/tradestats_2023.csv";
    let start_time = Instant::now();
    let file = File::open(file_path).expect("File open error");
    let mut  rdr = csv::ReaderBuilder::new()
        .delimiter(b',')  // Указываем разделитель
        .from_reader(file);
    let mut ts = TestTradingSystem::new();


    for candle in rdr.deserialize::<CandleTradeStats>() {
        match candle {
            Ok(record) => {
                ts.trade(record);
            }
            Err(err) => {
                eprintln!("Error deserializing record: {:?}", err);
            }
        }
    }

    let elapsed_time = start_time.elapsed();
    println!("financial_result : {:?}", ts.get_financial_result());
    println!("Total execution time: {:?}", elapsed_time);

}