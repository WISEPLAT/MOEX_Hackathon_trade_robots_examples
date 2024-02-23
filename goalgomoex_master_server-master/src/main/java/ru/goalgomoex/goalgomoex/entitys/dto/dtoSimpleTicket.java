package ru.goalgomoex.goalgomoex.entitys.dto;

import ru.goalgomoex.goalgomoex.entitys.goTicket;

public class dtoSimpleTicket implements IDTOEntity{
    private String SECID;
    private String SHORTNAME;
    private String SECNAME;

    public dtoSimpleTicket() {
    }

    public dtoSimpleTicket(String SECID, String SHORTNAME, String SECNAME) {
        this.SECID = SECID;
        this.SHORTNAME = SHORTNAME;
        this.SECNAME = SECNAME;
    }

    public dtoSimpleTicket(goTicket ticket) {
        this.SECID = ticket.getSECID();
        this.SHORTNAME = ticket.getSHORTNAME();
        this.SECNAME = ticket.getSECNAME();
    }

    public String getSECID() {
        return SECID;
    }

    public void setSECID(String SECID) {
        this.SECID = SECID;
    }

    public String getSHORTNAME() {
        return SHORTNAME;
    }

    public void setSHORTNAME(String SHORTNAME) {
        this.SHORTNAME = SHORTNAME;
    }

    public String getSECNAME() {
        return SECNAME;
    }

    public void setSECNAME(String SECNAME) {
        this.SECNAME = SECNAME;
    }
}
