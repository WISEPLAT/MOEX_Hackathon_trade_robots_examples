package ru.goalgomoex.goalgomoex.controllers.api.v1;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoSignal;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoSimpleTicket;
import ru.goalgomoex.goalgomoex.entitys.goSignal;
import ru.goalgomoex.goalgomoex.entitys.goTicket;
import ru.goalgomoex.goalgomoex.repository.GoSignalRepository;
import ru.goalgomoex.goalgomoex.repository.GoTicketRepository;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/api/v1/signal")
public class RestSignalsController {
    @Autowired
    private GoSignalRepository goSignalRepository;
    @PostMapping("/add")
    public dtoSignal add(@RequestBody dtoSignal signal){
        return goSignalRepository.saveAndFlush(new goSignal(signal)).getDto();
    }
    @GetMapping("/get")
    public dtoSignal get(@RequestParam("id") long id){
        return goSignalRepository.findById(id).orElse(new goSignal()).getDto();
    }
    @GetMapping("/list")
    public List<dtoSignal> getList(){
        List<dtoSignal> signals = new ArrayList<>();
        for (goSignal signal: goSignalRepository.findAll()) {
            signals.add(signal.getDto());
        }
        return signals;
    }
    @GetMapping("/list/ByTask")
    public List<dtoSignal> getListByTask(@RequestParam("task_id") long task_id){
        List<dtoSignal> signals = new ArrayList<>();
        for (goSignal signal: goSignalRepository.findAllByTaskId(task_id)) {
            signals.add(signal.getDto());
        }
        return signals;
    }
    @GetMapping("/list/byTicker")
    public List<dtoSignal> getListByTicket(@RequestParam("ticker") String ticker){
        List<dtoSignal> signals = new ArrayList<>();
        for (goSignal signal: goSignalRepository.findAllByTicker(ticker)) {
            signals.add(signal.getDto());
        }
        return signals;
    }
}
