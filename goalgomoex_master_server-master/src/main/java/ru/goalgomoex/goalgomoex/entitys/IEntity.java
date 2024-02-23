package ru.goalgomoex.goalgomoex.entitys;

public interface IEntity{
    long getID();
    String getGUID();
    int getVersion();
    void upVersion();
}
