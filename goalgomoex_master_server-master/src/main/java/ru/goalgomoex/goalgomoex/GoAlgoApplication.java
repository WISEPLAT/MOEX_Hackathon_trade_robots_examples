package ru.goalgomoex.goalgomoex;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.SchedulingException;
import org.springframework.scheduling.annotation.EnableScheduling;
import ru.goalgomoex.goalgomoex.services.ScheduleUpdateService;

@SpringBootApplication
@EnableScheduling
public class GoAlgoApplication {
	public static void main(String[] args) {
		SpringApplication.run(GoAlgoApplication.class, args);
	}
}
