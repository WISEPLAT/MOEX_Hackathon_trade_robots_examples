package ru.goalgomoex.goalgomoex.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.goalgomoex.goalgomoex.entitys.goSignal;
import ru.goalgomoex.goalgomoex.entitys.goTask;

import java.util.List;

@Repository
public interface GoSignalRepository extends JpaRepository<goSignal, Long> {
    List<goSignal> findAllByTaskId(long taskId);
    List<goSignal> findAllByTicker(String ticker);
}
