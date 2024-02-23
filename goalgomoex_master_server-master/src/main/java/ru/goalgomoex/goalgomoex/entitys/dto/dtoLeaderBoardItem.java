package ru.goalgomoex.goalgomoex.entitys.dto;

import javax.swing.*;

public class dtoLeaderBoardItem implements IDTOEntity{
    private String ticker;
    private double predict_price;
    private double predict_profit;
    private String timeframe;

    public dtoLeaderBoardItem() {
    }

    public dtoLeaderBoardItem(String ticker, double predict_price, double predict_profit, String timeframe) {
        this.ticker = ticker;
        this.predict_price = predict_price;
        this.predict_profit = predict_profit;
        this.timeframe = timeframe;
    }

    public String getTicker() {
        return ticker;
    }

    public void setTicker(String ticker) {
        this.ticker = ticker;
    }

    public double getPredict_price() {
        return predict_price;
    }

    public void setPredict_price(double predict_price) {
        this.predict_price = predict_price;
    }

    public double getPredict_profit() {
        return predict_profit;
    }

    public void setPredict_profit(double predict_profit) {
        this.predict_profit = predict_profit;
    }

    public String getTimeframe() {
        return timeframe;
    }

    public void setTimeframe(String timeframe) {
        this.timeframe = timeframe;
    }
}
