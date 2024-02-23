package ru.goalgomoex.goalgomoex.entitys;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import ru.goalgomoex.goalgomoex.core.GoTools;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoSignal;

@Entity
@Table(name = "go_signals")
public class goSignal implements IEntity{
    @Id
    @GeneratedValue
    private long ID;
    private String GUID;
    private int version;
    private long taskId;
    private String ticker;
    private int ansamble_signal;
    private int ansamble_signal_position;

    public goSignal(dtoSignal signal) {
        taskId = signal.getTask_id();
        ticker = signal.getTicker();
        ansamble_signal = signal.getAnsamble_signal();
        ansamble_signal_position = signal.getAnsamble_signal_position();
        GUID = GoTools.GenerateGUID();
    }

    public goSignal() {

    }

    public dtoSignal getDto(){
        return new dtoSignal(this);
    }
    @Override
    public long getID() {
        return ID;
    }

    @Override
    public String getGUID() {
        return GUID;
    }

    public void setID(long ID) {
        this.ID = ID;
    }

    public void setGUID(String GUID) {
        this.GUID = GUID;
    }

    @Override
    public int getVersion() {
        return version;
    }

    @Override
    public void upVersion() {
        version++;
    }

    public void setVersion(int version) {
        this.version = version;
    }

    public long getTaskId() {
        return taskId;
    }

    public void setTaskId(long task) {
        this.taskId = task;
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
