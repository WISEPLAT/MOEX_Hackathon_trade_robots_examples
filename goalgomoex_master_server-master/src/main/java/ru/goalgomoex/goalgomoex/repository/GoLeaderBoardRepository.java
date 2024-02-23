package ru.goalgomoex.goalgomoex.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.goalgomoex.goalgomoex.entitys.goLeaderBoardItem;

import java.util.List;

@Repository
public interface GoLeaderBoardRepository extends JpaRepository<goLeaderBoardItem, Long> {
    List<goLeaderBoardItem> findByTimeframe(String timeframe);
    List<goLeaderBoardItem> findByTicker(String ticker);
}
