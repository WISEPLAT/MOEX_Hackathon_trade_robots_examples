package ru.goalgomoex.goalgomoex.entitys.dto;

public class dtoMoexMarkets implements IDTOEntity{
    private dtoMoexSecurities securities;

    public dtoMoexSecurities getSecurities() {
        return securities;
    }

    public void setSecurities(dtoMoexSecurities securities) {
        this.securities = securities;
    }
}
