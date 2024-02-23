package ru.goalgomoex.goalgomoex.entitys.dto;

import ru.goalgomoex.goalgomoex.entitys.dto.IDTOEntity;

public class dtoData<D,V> implements IDTOEntity {
    private D X;
    private V Y;
    public dtoData() {
    }
    public dtoData(D x, V y) {
        X = x;
        Y = y;
    }
    public D getX() {
        return X;
    }

    public void setX(D x) {
        X = x;
    }

    public V getY() {
        return Y;
    }

    public void setY(V y) {
        Y = y;
    }
}
