package ru.goalgomoex.goalgomoex.controllers.api.v1;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import ru.goalgomoex.goalgomoex.core.GoTools;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoMessage;
import ru.goalgomoex.goalgomoex.entitys.goScriptConfig;
import ru.goalgomoex.goalgomoex.services.GoConfService;

import java.util.List;

@RestController
@RequestMapping("/api/v1/conf")
public class RestScriptConfController {
    @Autowired private GoConfService goConfService;
    @GetMapping("/list")
    public List<goScriptConfig> list(@RequestParam("service") String service){
        if(service == null || service.isEmpty()) return goConfService.list();
        return goConfService.listForService(service);
    }
    @GetMapping("/get")
    public goScriptConfig get(@RequestParam("id") long id){
        return goConfService.Get(id);
    }
    //public goScriptConfig addDef(@RequestParam("task_id") long task_id){
    //    return  new goScriptConfig()
    //            .setService("data_markup.py")
    //            .setTask_id(task_id)
    //            .setScaler_path("app/scalers/"+task_id+"/")
    //            .setNeural_path("app/neurals/"+task_id+"/")
    //            .setTicker("SBER")
    //            .setTimeframe("1D")
    //            .setStart_date("2023-11-01")
    //            .setEnd_date("2023-11-01")
    //            .setCount_points(6)
    //            .setExtr_bar_count(10)
    //            .setRespos_url("localhost:8080");
    //}
    @PostMapping("/add")
    public goScriptConfig add(@RequestBody goScriptConfig config){
        return  goConfService.createOrUpdate(
                config
                        .setVersion(0)
                        .setGUID(GoTools.GenerateGUID()));
    }
}
