package ru.goalgomoex.goalgomoex.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;

@Service
public class IOTaskJsonService {
    public String Read(long task_id){
        try {
            return new String(Files.readAllBytes(Path.of("results/"+task_id + ".json")));
        } catch (IOException e) {
            return null;
        }
    }
    public boolean Write(long task_id,String body){
        System.out.println("task_id "+task_id+"try write result");
        try {
            File file = new File("results/"+task_id+".json");
            System.out.println(file.getAbsolutePath());
            BufferedWriter writer = new BufferedWriter(new FileWriter(file.getPath()));
            writer.write(body);
            writer.close();
            return true;
        } catch (IOException e) {
            return false;
        }
    }
}
