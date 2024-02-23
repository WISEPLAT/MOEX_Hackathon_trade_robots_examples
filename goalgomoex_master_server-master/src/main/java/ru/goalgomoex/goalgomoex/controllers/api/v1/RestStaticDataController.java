package ru.goalgomoex.goalgomoex.controllers.api.v1;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoSimpleTicket;
import ru.goalgomoex.goalgomoex.entitys.goDuration;
import ru.goalgomoex.goalgomoex.entitys.goTicket;
import ru.goalgomoex.goalgomoex.repository.GoDurationRepository;
import ru.goalgomoex.goalgomoex.repository.GoTicketRepository;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/api/v1/data/lists")
public class RestStaticDataController {
    @Autowired private GoTicketRepository goTicketRepository;
    @Autowired private GoDurationRepository goDurationRepository;
    @GetMapping("/securities")
    public List<dtoSimpleTicket> getSecurities(){
        List<dtoSimpleTicket> list = new ArrayList<>();
        for (goTicket goTicket:goTicketRepository.findAll()) {list.add(new dtoSimpleTicket(goTicket));}
        return list;
    }
    @GetMapping("/securities/get")
    public goTicket getSecuritieById(@RequestParam("SECID") String SECID){
        return goTicketRepository.findById(SECID).orElse(null);
    }

    @GetMapping("/durations")
    public List<goDuration> getDurations(){
        return goDurationRepository.findAll();
    }
    @GetMapping("/simple/durations")
    public List<String> getSimpleDurations(){
        List<String> strings = new ArrayList<>();
        for (goDuration d:goDurationRepository.findAll()) {
            strings.add(d.getHint());
        }
        return strings;
    }
}
