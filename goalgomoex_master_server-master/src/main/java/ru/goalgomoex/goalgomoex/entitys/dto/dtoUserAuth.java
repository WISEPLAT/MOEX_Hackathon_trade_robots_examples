package ru.goalgomoex.goalgomoex.entitys.dto;

public class dtoUserAuth implements IDTOEntity{
    private String email;
    private String password;

    public dtoUserAuth() {
    }

    public dtoUserAuth(String email, String password) {
        this.email = email;
        this.password = password;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}
