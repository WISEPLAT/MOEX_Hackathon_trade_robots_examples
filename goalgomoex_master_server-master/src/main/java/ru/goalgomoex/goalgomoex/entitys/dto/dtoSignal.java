package ru.goalgomoex.goalgomoex.entitys.dto;

import ru.goalgomoex.goalgomoex.entitys.goSignal;

public class dtoSignal implements IDTOEntity{
    private long task_id;
    private String ticker;
    private int ansamble_signal;
    private int ansamble_signal_position;

    public dtoSignal() {
    }
    public dtoSignal(goSignal signal){
        task_id = signal.getTaskId();
        ticker = signal.getTicker();
        ansamble_signal = signal.getAnsamble_signal();
        ansamble_signal_position = signal.getAnsamble_signal_position();
    }

    public long getTask_id() {
        return task_id;
    }

    public void setTask_id(long task_id) {
        this.task_id = task_id;
    }

    public String getTicker() {
        return ticker;
    }

    public void setTicker(String ticker) {
        this.ticker = ticker;
    }

    public int getAnsamble_signal() {
        return ansamble_signal;
    }

    public void setAnsamble_signal(int ansamble_signal) {
        this.ansamble_signal = ansamble_signal;
    }

    public int getAnsamble_signal_position() {
        return ansamble_signal_position;
    }

    public void setAnsamble_signal_position(int ansamble_signal_position) {
        this.ansamble_signal_position = ansamble_signal_position;
    }
}
