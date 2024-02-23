package ru.goalgomoex.goalgomoex.entitys;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import ru.goalgomoex.goalgomoex.core.GoTools;
import ru.goalgomoex.goalgomoex.entitys.IEntity;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Entity
@Table(name = "go_script_configs")
public class goScriptConfig implements IEntity {
    @Id
    @GeneratedValue
    private long ID;
    private String GUID;
    private int version;
    private String service;

    //TODO USER ID

    private long task_id;
    private String scaler_path;
    private String neural_path;
    private String ticker;
    private String timeframe;
    private String start_date;
    private String end_date;
    private int count_points;
    private int extr_bar_count;
    private float max_unmark;
    private int size_df;
    private int count_days;
    private String data_path;
    private boolean new_model_flag;
    private float learning_rate;
    private int epochs;
    private int steps_per_epoch;
    private int validation_steps;
    private String respos_url;

    public goScriptConfig() {
        setGUID(GoTools.GenerateGUID());
        setVersion(0);
    }

    public String[] toParams() {
        List<String> param = new ArrayList<>();
        param.add("--cmd_config");
        try {
            for (Field f : this.getClass().getFields()) {
                param.add("--" + f.getName() + " " + f.get(f.getClass()).toString());
            }
        } catch (IllegalAccessException e) {
            throw new RuntimeException(e);
        }
        return param.toArray(String[]::new);
    }

    @Override
    public String toString() {
        return  "--cmd_config " +
                " --task_id " + task_id +
                " --scaler_path " + scaler_path +
                " --neural_path " + neural_path +
                " --ticker " + ticker  +
                " --timeframe " + timeframe  +
                " --start_date " + start_date +
                " --end_date " + end_date +
                " --count_points " + count_points +
                " --extr_bar_count " + extr_bar_count +
                " --max_unmark " + max_unmark +
                " --size_df " + size_df +
                " --count_days " + count_days +
                " --data_path " + data_path +
                " --new_model_flag " + new_model_flag +
                " --learning_rate " + learning_rate +
                " --epochs " + epochs +
                " --steps_per_epoch " + steps_per_epoch +
                " --validation_steps " + validation_steps +
                " --respos_url " + respos_url;
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

    public goScriptConfig setGUID(String GUID) {
        this.GUID = GUID;
        return this;
    }
    @Override
    public int getVersion() {
        return version;
    }

    @Override
    public void upVersion() {
        version++;
    }

    public goScriptConfig setVersion(int version) {
        this.version = version;
        return this;
    }

    public long getTask_id() {
        return task_id;
    }

    public goScriptConfig setTask_id(long task_id) {
        this.task_id = task_id;
        return this;
    }

    public String getScaler_path() {
        return scaler_path;
    }

    public goScriptConfig setScaler_path(String scaler_path) {
        this.scaler_path = scaler_path;
        return this;
    }

    public String getNeural_path() {
        return neural_path;
    }

    public goScriptConfig setNeural_path(String neural_path) {
        this.neural_path = neural_path;
        return this;
    }

    public String getTicker() {
        return ticker;
    }

    public goScriptConfig setTicker(String ticker) {
        this.ticker = ticker;
        return this;
    }

    public String getTimeframe() {
        return timeframe;
    }

    public goScriptConfig setTimeframe(String timeframe) {
        this.timeframe = timeframe;
        return this;
    }

    public String getStart_date() {
        return start_date;
    }

    public goScriptConfig setStart_date(String start_date) {
        this.start_date = start_date;
        return this;
    }

    public String getEnd_date() {
        return end_date;
    }

    public goScriptConfig setEnd_date(String end_date) {
        this.end_date = end_date;
        return this;
    }

    public int getCount_points() {
        return count_points;
    }

    public goScriptConfig setCount_points(int count_points) {
        this.count_points = count_points;
        return this;
    }

    public int getExtr_bar_count() {
        return extr_bar_count;
    }

    public goScriptConfig setExtr_bar_count(int extr_bar_count) {
        this.extr_bar_count = extr_bar_count;
        return this;
    }

    public float getMax_unmark() {
        return max_unmark;
    }

    public goScriptConfig setMax_unmark(float max_unmark) {
        this.max_unmark = max_unmark;
        return this;
    }

    public int getSize_df() {
        return size_df;
    }

    public goScriptConfig setSize_df(int size_df) {
        this.size_df = size_df;
        return this;
    }

    public int getCount_days() {
        return count_days;
    }

    public goScriptConfig setCount_days(int count_days) {
        this.count_days = count_days;
        return this;
    }

    public String getData_path() {
        return data_path;
    }

    public goScriptConfig setData_path(String data_path) {
        this.data_path = data_path;
        return this;
    }

    public boolean isNew_model_flag() {
        return new_model_flag;
    }

    public goScriptConfig setNew_model_flag(boolean new_model_flag) {
        this.new_model_flag = new_model_flag;
        return this;
    }

    public float getLearning_rate() {
        return learning_rate;
    }

    public goScriptConfig setLearning_rate(float learning_rate) {
        this.learning_rate = learning_rate;
        return this;
    }

    public int getEpochs() {
        return epochs;
    }

    public goScriptConfig setEpochs(int epochs) {
        this.epochs = epochs;
        return this;
    }

    public int getSteps_per_epoch() {
        return steps_per_epoch;
    }

    public goScriptConfig setSteps_per_epoch(int steps_per_epoch) {
        this.steps_per_epoch = steps_per_epoch;
        return this;
    }

    public int getValidation_steps() {
        return validation_steps;
    }

    public goScriptConfig setValidation_steps(int validation_steps) {
        this.validation_steps = validation_steps;
        return this;
    }

    public String getRespos_url() {
        return respos_url;
    }

    public goScriptConfig setRespos_url(String respos_url) {
        this.respos_url = respos_url;
        return this;
    }

    public String getService() {
        return service;
    }

    public goScriptConfig setService(String service) {
        this.service = service;
        return this;
    }
}
