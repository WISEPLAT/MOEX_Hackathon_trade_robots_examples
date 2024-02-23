package ru.goalgomoex.goalgomoex.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.goalgomoex.goalgomoex.entitys.goTask;

import java.util.List;

@Repository
public interface GoTaskRepository extends JpaRepository<goTask, Long> {
    List<goTask> findByStatus(int status);
}
