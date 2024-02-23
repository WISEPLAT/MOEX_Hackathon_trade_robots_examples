package ru.goalgomoex.goalgomoex.controllers.api.v1;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoLeaderBoardItem;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoMessage;
import ru.goalgomoex.goalgomoex.entitys.goLeaderBoardItem;
import ru.goalgomoex.goalgomoex.services.GoLeaderBoardService;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@RestController
@RequestMapping("/api/v1/leaderboard")
public class RestLeaderBoardController {
    @Autowired private GoLeaderBoardService goLeaderBoardService;
    @GetMapping
    public List<dtoLeaderBoardItem> get(){
        List<dtoLeaderBoardItem> list = new ArrayList<>();
        for (goLeaderBoardItem go:
        goLeaderBoardService.list()) {
            list.add(go.getDto());
        }
        return list;
    }
    @GetMapping("/byTimeFrame")
    public List<dtoLeaderBoardItem> getByTimeframe(@RequestParam("tf") String timeframe){
        List<dtoLeaderBoardItem> list = new ArrayList<>();
        for (goLeaderBoardItem go:
                goLeaderBoardService.listByTimeframe(timeframe)) {
            list.add(go.getDto());
        }
        return list;
    }
    @DeleteMapping("/RemoveByDateAndTicker")
    public dtoMessage remove(@RequestParam("ticker") String timeframe,@RequestParam("date") Date date){
        goLeaderBoardService.RemoveByDateAndTicker(timeframe,date);
        return new dtoMessage("INFO","DONE");
    }

    @PostMapping
    public dtoMessage post(@RequestBody List<dtoLeaderBoardItem> itemList){
        List<goLeaderBoardItem> list = new ArrayList<>();
        for (dtoLeaderBoardItem dto:itemList) {
            list.add(new goLeaderBoardItem(dto));
        }
        if(!goLeaderBoardService.createOrUpdate(list).isEmpty())
            return new dtoMessage("INFO","DONE");
            else return new dtoMessage("ERROR","NOT DONE");
    }
}
