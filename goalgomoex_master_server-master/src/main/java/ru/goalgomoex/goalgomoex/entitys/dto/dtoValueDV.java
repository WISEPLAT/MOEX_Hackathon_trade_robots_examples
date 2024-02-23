package ru.goalgomoex.goalgomoex.entitys.dto;

import ru.goalgomoex.goalgomoex.entitys.dto.IDTOEntity;

public class dtoValueDV<T> implements IDTOEntity {
    private String description;
    private T values;
    public dtoValueDV(String description, T values) {
        this.description = description;
        this.values = values;
    }
    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public T getValues() {
        return values;
    }

    public void setValues(T values) {
        this.values = values;
    }
}
