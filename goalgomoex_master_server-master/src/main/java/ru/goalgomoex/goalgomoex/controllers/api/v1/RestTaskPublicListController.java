package ru.goalgomoex.goalgomoex.controllers.api.v1;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import ru.goalgomoex.goalgomoex.entitys.goTask;
import ru.goalgomoex.goalgomoex.services.GoTaskService;

import java.util.List;
@RestController
@RequestMapping("/api/v1/task/lists")
public class RestTaskPublicListController {

    @Autowired
    private GoTaskService goTaskService;
    @GetMapping("/all")
    public List<goTask> goTaskAllList(){
        return goTaskService.taskList();
    }
    @GetMapping("/wait")
    public List<goTask> goTaskWaitlist(){
        return goTaskService.taskWaitList();
    }
    @GetMapping("/inProgress")
    public List<goTask> goTaskInProgresslist(){
        return goTaskService.taskInProgressList();
    }
    @GetMapping("/done")
    public List<goTask> goTaskDonelist(){
        return goTaskService.taskDoneList();
    }
    @GetMapping("/withError")
    public List<goTask> goTaskDoneWithErrorlist(){
        return goTaskService.taskDoneWithErrorList();
    }
    @GetMapping("/doneWithError")
    public List<goTask> goTaskDoneAllList(){
        return goTaskService.taskDoneAllList();
    }

}
