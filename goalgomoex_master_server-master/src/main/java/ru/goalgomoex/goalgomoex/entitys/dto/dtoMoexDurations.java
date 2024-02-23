package ru.goalgomoex.goalgomoex.entitys.dto;

import java.util.ArrayList;

public class dtoMoexDurations {
    private ArrayList<ArrayList<Object>> data;
    public dtoMoexDurations() {
    }
    public dtoMoexDurations(ArrayList<ArrayList<Object>> data) {
        this.data = data;
    }
    public ArrayList<ArrayList<Object>> getData() {
        return data;
    }

    public void setData(ArrayList<ArrayList<Object>> data) {
        this.data = data;
    }
}
