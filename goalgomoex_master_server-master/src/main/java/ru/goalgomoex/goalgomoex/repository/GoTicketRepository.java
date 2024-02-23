package ru.goalgomoex.goalgomoex.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.goalgomoex.goalgomoex.entitys.goTicket;

@Repository
public interface GoTicketRepository extends JpaRepository<goTicket, String> {
}
