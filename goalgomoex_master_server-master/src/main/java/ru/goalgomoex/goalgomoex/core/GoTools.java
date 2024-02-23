package ru.goalgomoex.goalgomoex.core;

import com.google.gson.Gson;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class GoTools {
    public static String GenerateGUID(){
        return java.util.UUID.randomUUID().toString();
    }
}
