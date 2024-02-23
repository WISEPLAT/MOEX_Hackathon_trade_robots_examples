package ru.goalgomoex.goalgomoex.entitys.dto.task;

public class dtoTaskOut implements IDTOTaskOut{
    private long task_id;
    public dtoTaskOut() {}
    public dtoTaskOut(long task_id) {
        this.task_id = task_id;
    }
    public long getTask_id() {
        return task_id;
    }
    public void setTask_id(long task_id) {
        this.task_id = task_id;
    }
}
