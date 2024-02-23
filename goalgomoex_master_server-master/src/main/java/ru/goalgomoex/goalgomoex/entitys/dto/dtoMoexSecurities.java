package ru.goalgomoex.goalgomoex.entitys.dto;

import java.util.ArrayList;

public class dtoMoexSecurities implements IDTOEntity {
    private ArrayList<String> columns;
    private ArrayList<ArrayList<Object>> data;

    public ArrayList<String> getColumns() {
        return columns;
    }

    public void setColumns(ArrayList<String> columns) {
        this.columns = columns;
    }

    public ArrayList<ArrayList<Object>> getData() {
        return data;
    }

    public void setData(ArrayList<ArrayList<Object>> data) {
        this.data = data;
    }
}
