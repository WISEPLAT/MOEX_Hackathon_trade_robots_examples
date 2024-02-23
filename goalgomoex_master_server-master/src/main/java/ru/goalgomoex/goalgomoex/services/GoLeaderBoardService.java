package ru.goalgomoex.goalgomoex.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import ru.goalgomoex.goalgomoex.entitys.goLeaderBoardItem;
import ru.goalgomoex.goalgomoex.entitys.goScriptConfig;
import ru.goalgomoex.goalgomoex.repository.GoConfRepository;
import ru.goalgomoex.goalgomoex.repository.GoLeaderBoardRepository;

import java.util.Date;
import java.util.List;

@Service
public class GoLeaderBoardService {
    @Autowired private GoLeaderBoardRepository goLeaderBoardRepository;
    public List<goLeaderBoardItem> list(){
        return goLeaderBoardRepository.findAll();
    }
    public List<goLeaderBoardItem> listByTimeframe(String timeframe){
        return goLeaderBoardRepository.findByTimeframe(timeframe).stream().filter(x->x.getCreate_date().getDate()==new Date().getDate()).toList();
    }
    public void RemoveByDateAndTicker(String ticker,Date date){
        goLeaderBoardRepository.deleteAll(
                goLeaderBoardRepository.findByTicker(ticker).stream().filter(x->x.getCreate_date().getDate()==date.getDate()).toList()
        );
    }
    public goLeaderBoardItem createOrUpdate(goLeaderBoardItem object){
        if(object == null) return null;
        object.upVersion();
        return goLeaderBoardRepository.saveAndFlush(object);
    }
    public List<goLeaderBoardItem> createOrUpdate(List<goLeaderBoardItem> object){
        if(object == null) return null;
        object.forEach(x->
                {
                    x.setCreate_date(new Date());
                    x.upVersion();
                }
        );
        return goLeaderBoardRepository.saveAllAndFlush(object);
    }
    public goLeaderBoardItem Get(long id) {
        return goLeaderBoardRepository.findById(id).orElse(new goLeaderBoardItem());
    }
}
