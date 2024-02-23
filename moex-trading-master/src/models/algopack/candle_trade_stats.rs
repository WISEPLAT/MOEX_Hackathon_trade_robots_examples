use serde::Deserialize;
#[derive(Debug, Deserialize)]
pub struct CandleTradeStats  {
    pub tradedate: String, //0
    pub tradetime: String, //1
    pub secid: String, //2
    pub pr_open: Option<f64>, //3
    pub pr_high: Option<f64>, //4
    pub pr_low: Option<f64>, //5
    pub pr_close: Option<f64>, //6
    pub pr_std: Option<f64>, //7
    pub vol: Option<f64>, //8
    pub val: Option<f64>, //9
    pub trades: Option<f64>, //10
    pub pr_vwap: Option<f64>, //11
    pub pr_change: Option<f64>, //12
    pub trades_b: Option<f64>, //13
    pub trades_s: Option<f64>, //14
    pub val_b: Option<f64>, //15
    pub val_s: Option<f64>, //16
    pub vol_b: Option<f64>, //17
    pub vol_s: Option<f64>, //18
    pub disb: Option<f64>, //19
    pub pr_vwap_b: Option<f64>, //20
    pub pr_vwap_s: Option<f64>, //21
    pub systime: Option<String>, //22
}