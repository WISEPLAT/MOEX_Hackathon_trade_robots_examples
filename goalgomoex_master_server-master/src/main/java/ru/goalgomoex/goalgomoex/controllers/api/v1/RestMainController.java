package ru.goalgomoex.goalgomoex.controllers.api.v1;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import ru.goalgomoex.goalgomoex.entitys.goScriptConfig;
import ru.goalgomoex.goalgomoex.services.PythonStarter;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoMessage;

import java.util.Date;

@RestController
@RequestMapping("/api/v1")
public class RestMainController{
    @Autowired protected PythonStarter pythonStarter;
    @GetMapping("/")
    public dtoMessage getTitle(){
        return new dtoMessage("INFO","GOALGOMOEX");
    }
    @GetMapping("/version")
    public dtoMessage getVersion(){
        return new dtoMessage("INFO","v1");
    }
}
