package ru.goalgomoex.goalgomoex.entitys;

import jakarta.persistence.*;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

@Entity
public class goUserAuthData implements UserDetails, IEntity{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String GUID;
    private int version;
    private String username;
    private String password;
    private String displayableUsername;
    private boolean enabled;
    private String roles;

    public goUserAuthData(){
        enabled = true;
    }
    public goUserAuthData(String displayableUsername, String username, String password) {
        this.username = username;
        this.password = password;
        this.displayableUsername = displayableUsername;
        enabled = true;
    }


    public String getUsername() {
        return username;
    }

    public String getDisplayableUsername() {
        return displayableUsername;
    }

    public void setDisplayableUsername(String displayableUsername) {
        this.displayableUsername = displayableUsername;
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return isAccountNonExpired();
    }

    @Override
    public boolean isEnabled() {
        return enabled;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return Collections.singleton(new goRole(roles,roles));
    }
    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public void setRoles(goRole roles) {
        this.roles = roles.getAuthority();
    }

    @Override
    public long getID() {
        return id;
    }

    @Override
    public String getGUID() {
        return GUID;
    }

    @Override
    public int getVersion() {
        return version;
    }

    @Override
    public void upVersion() {
        version++;
    }

    public void setEnabled(boolean value) {
        enabled = value;
    }
}
