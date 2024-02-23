package ru.goalgomoex.goalgomoex.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.goalgomoex.goalgomoex.entitys.goScriptConfig;
import ru.goalgomoex.goalgomoex.entitys.goTask;

import java.util.List;

@Repository
public interface GoConfRepository extends JpaRepository<goScriptConfig, Long> {
    List<goScriptConfig> findByService(String service);
}
