package ru.goalgomoex.goalgomoex.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import ru.goalgomoex.goalgomoex.entitys.goTask;
import ru.goalgomoex.goalgomoex.repository.GoTaskRepository;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Optional;

@Service
public class GoTaskService {
    @Autowired private GoTaskRepository goTaskRepository;
    @Autowired private PythonStarter pythonStarter;
    public List<goTask> taskList() {return goTaskRepository.findAll();}
    public List<goTask> taskWaitList() {return goTaskRepository.findByStatus(0);}
    public List<goTask> taskInProgressList() {
        ArrayList<goTask> temp = new ArrayList<>();
        temp.addAll(goTaskRepository.findByStatus(1));
        temp.addAll(goTaskRepository.findByStatus(4));
        return temp;
    }
    public List<goTask> taskDoneList() {return goTaskRepository.findByStatus(2);}
    public List<goTask> taskDoneWithErrorList() {return goTaskRepository.findByStatus(3);}
    public goTask getTask(long id){
        return goTaskRepository.findById(id).orElse(null);
    }

    public List<goTask> taskDoneAllList() {
        ArrayList<goTask> temp = new ArrayList<>();
        temp.addAll(goTaskRepository.findByStatus(2));
        temp.addAll(goTaskRepository.findByStatus(3));
        return temp;
    }
    public goTask createOrUpdate(goTask object){
        if(object == null) return null;
        object.upVersion();
        return goTaskRepository.saveAndFlush(object);
    }
    public void taskInProgress(Long ID,long pid) {
        Optional<goTask> task = goTaskRepository.findById(ID);
        if (task.isEmpty()) return;
        goTask t = task.get();
        t.setProcessID(String.valueOf(pid));
        t.setStatus(1);
        t.setStart_time(new Date());
        createOrUpdate(t);
    }
    public void taskComplied(Long ID){
        sysTaskComplied(ID,2);
    }
    public void taskCompliedWithError(Long ID){
        Optional<goTask> task = goTaskRepository.findById(ID);
        sysTaskComplied(ID,3);
        pythonStarter.Kill(task.get().getProcessID());
    }
    private void sysTaskComplied(Long ID, int status){
        Optional<goTask> task = goTaskRepository.findById(ID);
        if(task.isEmpty()) return;
        goTask t = task.get();
        t.setStatus(status);
        t.setEnd_time(new Date());
        createOrUpdate(t);
    }
    @Scheduled(fixedRate = 10000)
    private void TaskManager(){
        if(!goTaskRepository.findByStatus(1).isEmpty()) return;
        if(goTaskRepository.findByStatus(0).isEmpty()) return;
        for (goTask task:goTaskRepository.findByStatus(0)) {
            if(task.getConfig() == null) continue;
            Process rs = pythonStarter.Start(task.getID(),task.getConfig());
            if(rs != null) {
                taskInProgress(task.getID(),rs.pid());
                if(task.getConfig().getService().equals("calc_signals.py")) task.setStatus(4);
            }else {
                task.setStart_time(new Date());
                task.setEnd_time(new Date());
                task.setStatus(3);
                createOrUpdate(task);
            }
            break;
        }
    }

}
