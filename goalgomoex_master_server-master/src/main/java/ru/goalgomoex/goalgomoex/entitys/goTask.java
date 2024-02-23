package ru.goalgomoex.goalgomoex.entitys;

import jakarta.persistence.*;

import java.util.Date;

@Entity
@Table(name = "go_tasks")
public class goTask implements IEntity{
    @Id
    @GeneratedValue
    private long ID;
    private String GUID;
    private int version;
    private String processID;
    //TODO USER ID

    /* *
    * STATUS
    * 0 - В очереди
    * 1 - В работе
    * 2 - Завершен
    * 3 - С ошибкой
    * 4 - Постоянный
    * */
    private int status;

    @ManyToOne(targetEntity = goScriptConfig.class)
    private goScriptConfig config;

    private Date start_time;
    private Date end_time;

    public goTask() {
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
        return GUID;
    }

    public void setGUID(String GUID) {
        this.GUID = GUID;
    }
    @Override
    public int getVersion() {
        return version;
    }

    public void setVersion(int version) {
        this.version = version;
    }

    public String getProcessID() {
        return processID;
    }

    public void setProcessID(String processID) {
        this.processID = processID;
    }

    public int getStatus() {
        return status;
    }

    public void setStatus(int status) {
        this.status = status;
    }

    @Override
    public void upVersion() {
        version++;
    }

    public Date getStart_time() {
        return start_time;
    }

    public void setStart_time(Date start_time) {
        this.start_time = start_time;
    }

    public Date getEnd_time() {
        return end_time;
    }

    public void setEnd_time(Date end_time) {
        this.end_time = end_time;
    }

    public goScriptConfig getConfig() {
        return config;
    }

    public void setConfig(goScriptConfig config) {
        this.config = config;
    }
}
