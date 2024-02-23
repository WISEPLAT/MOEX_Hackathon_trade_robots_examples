package ru.goalgomoex.goalgomoex.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import ru.goalgomoex.goalgomoex.entitys.goScriptConfig;
import ru.goalgomoex.goalgomoex.entitys.goTask;
import ru.goalgomoex.goalgomoex.repository.GoConfRepository;
import ru.goalgomoex.goalgomoex.repository.GoTaskRepository;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Optional;

@Service
public class GoConfService {
    @Autowired private GoConfRepository goConfRepository;
    public List<goScriptConfig> list(){
        return goConfRepository.findAll();
    }
    public List<goScriptConfig> listForService(String service){
        return goConfRepository.findByService(service);
    }
    public goScriptConfig createOrUpdate(goScriptConfig object){
        if(object == null) return null;
        object.upVersion();
        return goConfRepository.saveAndFlush(object);
    }
    public goScriptConfig Get(long id) {
        return goConfRepository.findById(id).orElse(new goScriptConfig());
    }
}
