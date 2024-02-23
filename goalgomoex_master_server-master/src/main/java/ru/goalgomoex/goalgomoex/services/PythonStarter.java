package ru.goalgomoex.goalgomoex.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import ru.goalgomoex.goalgomoex.entitys.goScriptConfig;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Service
public class PythonStarter {
    public Process Start(long task_id,goScriptConfig config){
        ArrayList<String> UNIX = new ArrayList<>();
        UNIX.add("/bin/sh");
        UNIX.add("/var/opt/goalgomoex/starter.sh");
        UNIX.add(config.getService());
        UNIX.add(config.toString());
        try {
            Process process = Runtime.getRuntime().exec(String.join(" ",UNIX));
            System.out.println(String.join(" ",UNIX));
            return process;
        } catch (Exception e) {
            System.out.println(e.getMessage());
            return null;
        }
    }
    public void Kill(String processId){
        ArrayList<String> UNIX = new ArrayList<>();
        UNIX.add("/bin/sh");
        UNIX.add("kill");
        UNIX.add(processId);
        try {
            Process process = Runtime.getRuntime().exec(String.join(" ",UNIX));
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}
