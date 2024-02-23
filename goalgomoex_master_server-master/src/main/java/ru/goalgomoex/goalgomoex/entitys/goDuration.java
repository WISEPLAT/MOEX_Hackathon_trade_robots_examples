package ru.goalgomoex.goalgomoex.entitys;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "go_durations")
public class goDuration implements IEntity{

    private long ID;
    private double interval;
    private double duration;
    private double days;
    private String title;
    @Id
    private String hint;

    public goDuration() {
    }

    public goDuration(long ID, double interval, double duration, double days, String title, String hint) {
        this.ID = ID;
        this.interval = interval;
        this.duration = duration;
        this.days = days;
        this.title = title;
        this.hint = hint;
    }

    @Override
    public long getID() {
        return ID;
    }

    public void setID(long ID) {
        this.ID = ID;
    }

    @Override
    public String getGUID() {
        return null;
    }

    @Override
    public int getVersion() {
        return 0;
    }

    @Override
    public void upVersion() {

    }

    public double getInterval() {
        return interval;
    }

    public void setInterval(double interval) {
        this.interval = interval;
    }

    public double getDuration() {
        return duration;
    }

    public void setDuration(double duration) {
        this.duration = duration;
    }

    public double getDays() {
        return days;
    }

    public void setDays(double days) {
        this.days = days;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getHint() {
        return hint;
    }

    public void setHint(String hint) {
        this.hint = hint;
    }
}
