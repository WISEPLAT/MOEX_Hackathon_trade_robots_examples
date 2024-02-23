package ru.goalgomoex.goalgomoex.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.goalgomoex.goalgomoex.entitys.goUserAuthData;

public interface GoUserAuthRepository extends JpaRepository<goUserAuthData, Long> {
    goUserAuthData findByUsername(String username);
    Boolean existsByUsername(String username);
}
