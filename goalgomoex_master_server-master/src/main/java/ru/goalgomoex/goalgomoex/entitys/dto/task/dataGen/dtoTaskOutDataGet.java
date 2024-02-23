package ru.goalgomoex.goalgomoex.entitys.dto.task.dataGen;

import ru.goalgomoex.goalgomoex.entitys.dto.task.dtoTaskOut;

public class dtoTaskOutDataGet extends dtoTaskOut {
    private String status;

    public dtoTaskOutDataGet() {
    }

    public dtoTaskOutDataGet(long task_id) {
        super(task_id);
    }
    public dtoTaskOutDataGet(String status) {
        this.status = status;
    }

    public dtoTaskOutDataGet(long task_id, String status) {
        super(task_id);
        this.status = status;
    }
    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
