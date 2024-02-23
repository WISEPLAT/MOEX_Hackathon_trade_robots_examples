package ru.goalgomoex.goalgomoex.controllers.api.v1;


import com.google.gson.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import ru.goalgomoex.goalgomoex.core.GoTools;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoMessage;
import ru.goalgomoex.goalgomoex.entitys.dto.task.dtoTaskOut;
import ru.goalgomoex.goalgomoex.entitys.goScriptConfig;
import ru.goalgomoex.goalgomoex.entitys.goTask;
import ru.goalgomoex.goalgomoex.services.GoConfService;
import ru.goalgomoex.goalgomoex.services.GoTaskService;
import ru.goalgomoex.goalgomoex.services.IOTaskJsonService;

import java.util.Date;
import java.util.List;

@RestController
@RequestMapping("/api/v1/task")
public class RestTaskController {
    @Autowired
    private GoTaskService goTaskService;
    @Autowired
    private GoConfService goConfService;
    @Autowired
    private IOTaskJsonService ioTaskJsonService;
    @GetMapping("/add")
    public goTask goTaskAdd(){
        goTask task = new goTask();
        task.setStatus(0);
        task.setGUID(GoTools.GenerateGUID());
        task.setVersion(0);
        return goTaskService.createOrUpdate(task);
    }
    @GetMapping("/get")
    public goTask getGoTask(@RequestParam("task_id") long task_id){
        return goTaskService.getTask(task_id);
    }
    @GetMapping("/close")
    public dtoMessage TaskClose(@RequestParam("task_id") long task_id){
        goTaskService.taskCompliedWithError(task_id);
        return new dtoMessage("INFO","Task %d Close".formatted(task_id));
    }
    @GetMapping("/setConfig")
    public dtoMessage start(@RequestParam("task_id") long task_id,@RequestParam("conf_id") long conf_id){
        goTask task = goTaskService.getTask(task_id);
        goScriptConfig config = goConfService.Get(conf_id);
        config.setTask_id(task_id);
        task.setConfig(config);
        goConfService.createOrUpdate(config);
        goTaskService.createOrUpdate(task);
        return new dtoMessage("INFO","DONE");
    }
    @GetMapping(path = "/result",produces= MediaType.APPLICATION_JSON_VALUE)
    public String TaskResult(@RequestParam("task_id") long task_id){
        return ioTaskJsonService.Read(task_id);
    }
    @PostMapping("/complied")
    public dtoMessage TaskComplied(@RequestBody String taskAsJson){
        Gson gson = new Gson();
        dtoTaskOut task = gson.fromJson(taskAsJson,dtoTaskOut.class);
        goTaskService.taskComplied(task.getTask_id());
        if(ioTaskJsonService.Write(task.getTask_id(),taskAsJson))
        return new dtoMessage("INFO","Task %d Complied".formatted(task.getTask_id()));
        else return new dtoMessage("INFO","Task %d Complied but cannot save result".formatted(task.getTask_id()));
    }
}
