package ru.goalgomoex.goalgomoex.services;

import com.google.gson.Gson;
import jakarta.annotation.PostConstruct;
import jakarta.validation.constraints.Null;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoMoexDurations;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoMoexIndex;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoMoexMarkets;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoMoexSecurities;
import ru.goalgomoex.goalgomoex.entitys.goDuration;
import ru.goalgomoex.goalgomoex.entitys.goTicket;
import ru.goalgomoex.goalgomoex.repository.GoDurationRepository;
import ru.goalgomoex.goalgomoex.repository.GoTicketRepository;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;

@Service
@Component
public class ScheduleUpdateService {
    public static String URL_securities = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json";
    public static String URL_Durations = "https://iss.moex.com/iss/index.json";
    @Autowired private GoTicketRepository goTicketRepository;
    @Autowired private GoDurationRepository goDurationRepository;
    @PostConstruct
    public void init() {
        System.out.println("INIT SYNC API");
        UpdateSecurities();
        System.out.println("DONE UpdateSecurities");
        UpdateDurations();
        System.out.println("DONE UpdateDurations");
    }
    @Scheduled(cron = "@daily")
    @Async
    public void UpdateSecurities(){
        try (InputStream input = new URL(URL_securities).openStream()) {
            InputStreamReader isr = new InputStreamReader(input);
            BufferedReader reader = new BufferedReader(isr);
            Gson gson = new Gson();
            dtoMoexMarkets moexMarkets = gson.fromJson(reader, dtoMoexMarkets.class);
            dtoMoexSecurities moexSecurities = moexMarkets.getSecurities();
            List<goTicket> tickets = new ArrayList<>();
            for (ArrayList<Object> row:moexSecurities.getData()) {
                for (Object d:row) {if(d == null) d = 0;}
                tickets.add(new goTicket(
                        (String) dGet("",row.get(0)), (String)  dGet("",row.get(1)),
                        (String) dGet("",row.get(2)), (Double)  dGet(0d,row.get(3)),
                        (Double) dGet(0d,row.get(4)), (Double)  dGet(0d,row.get(5)),
                        (String) dGet("",row.get(6)), (String)  dGet("",row.get(7)),
                        (Double) dGet(0d,row.get(8)), (String)  dGet("",row.get(9)),
                        (String) dGet("",row.get(10)),(String)  dGet("", row.get(11)),
                        (String) dGet("",row.get(12)),(String)  dGet("", row.get(13)),
                        (Double) dGet(0d,row.get(14)),(Double)  dGet(0d,row.get(15)),
                        (String) dGet("",row.get(16)),(String)  dGet("", row.get(17)),
                        (Double) dGet(0d,row.get(18)),(String)  dGet("", row.get(19)),
                        (String) dGet("",row.get(20)),(String)  dGet("", row.get(21)),
                        (Double) dGet(0d,row.get(22)),(String)  dGet("",row.get(23)),
                        (String) dGet("",row.get(24)),(Double)  dGet(0d,row.get(25)),
                        (String) dGet("",row.get(26))));}
            goTicketRepository.saveAllAndFlush(tickets);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
    @Scheduled(cron = "@daily")
    @Async
    public void UpdateDurations(){
        try (InputStream input = new URL(URL_Durations).openStream()) {
            InputStreamReader isr = new InputStreamReader(input);
            BufferedReader reader = new BufferedReader(isr);
            Gson gson = new Gson();
            dtoMoexIndex index = gson.fromJson(reader, dtoMoexIndex.class);
            dtoMoexDurations moexDurations = index.getDurations();
            List<goDuration> durations = new ArrayList<>();
            int i = 0;
            for (ArrayList<Object> row:moexDurations.getData()) {
                durations.add(new goDuration(i++,
                        (Double) dGet(0d,row.get(0)),
                        (Double) dGet(0d,row.get(1)),
                        (Double) dGet(0d,row.get(2)),
                        (String) dGet("",row.get(3)),
                        (String) dGet("",row.get(4))));
            }
            goDurationRepository.saveAllAndFlush(durations);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
    private Object dGet(Object def,Object object){
        return object==null?def:object;
    }
}
