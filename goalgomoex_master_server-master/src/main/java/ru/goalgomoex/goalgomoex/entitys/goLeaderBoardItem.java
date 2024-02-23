package ru.goalgomoex.goalgomoex.entitys;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoLeaderBoardItem;

import java.util.Date;


@Entity
@Table(name = "go_leaderboard_items")
public class goLeaderBoardItem implements IEntity{
    @Id
    @GeneratedValue
    private long ID;
    private String GUID;
    private int version;
    private String ticker;
    private double predict_price;
    private double predict_profit;
    private String timeframe;
    private Date create_date;

    public goLeaderBoardItem() {
    }
    public goLeaderBoardItem(dtoLeaderBoardItem dto) {
        this.ticker = dto.getTicker();
        this.predict_price = dto.getPredict_price();
        this.predict_profit = dto.getPredict_profit();
        this.timeframe = dto.getTimeframe();
    }
    public goLeaderBoardItem(String ticker, double predict_price, double predict_profit, String timeframe) {
        this.ticker = ticker;
        this.predict_price = predict_price;
        this.predict_profit = predict_profit;
        this.timeframe = timeframe;
    }
    public dtoLeaderBoardItem getDto(){
        return new dtoLeaderBoardItem(ticker,predict_price,predict_profit,timeframe);
    }
    @Override
    public long getID() {
        return ID;
    }

    public void setID(long ID) {
        this.ID = ID;
    }

    public void setGUID(String GUID) {
        this.GUID = GUID;
    }

    public void setVersion(int version) {
        this.version = version;
    }

    @Override
    public String getGUID() {
        return GUID;
    }

    @Override
    public int getVersion() {
        return version;
    }

    @Override
    public void upVersion() {
        version++;
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

    public Date getCreate_date() {
        return create_date;
    }

    public void setCreate_date(Date create_date) {
        this.create_date = create_date;
    }
}
