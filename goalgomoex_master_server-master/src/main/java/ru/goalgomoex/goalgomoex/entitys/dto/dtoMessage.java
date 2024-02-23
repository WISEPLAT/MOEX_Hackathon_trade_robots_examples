package ru.goalgomoex.goalgomoex.entitys.dto;

import java.util.Date;

public class dtoMessage implements IDTOEntity {
    private final String Type;
    private final String Message;
    private final Date serverDateTime;
    public dtoMessage(String Type,String Message) {
        this.Type = Type;
        this.Message = Message;
        this.serverDateTime = new Date();
    }

    public String getType() {
        return Type;
    }

    public String getMessage() {
        return Message;
    }

    public Date getServerDateTime() {
        return serverDateTime;
    }
}
