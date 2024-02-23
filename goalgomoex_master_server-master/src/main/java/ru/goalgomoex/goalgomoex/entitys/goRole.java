package ru.goalgomoex.goalgomoex.entitys;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import org.springframework.security.core.GrantedAuthority;

@Entity
@Table(name = "go_role")
public class goRole implements GrantedAuthority, IEntity{
    @Id
    @GeneratedValue
    private Long ID;
    private String code;
    private String GUID;
    private String title;
    private int version;

    public goRole(String code, String title) {
        this.code = code;
        this.title = title;
    }

    @Override
    public String getAuthority() {
        return code;
    }
    public String getTitle() {
        return title;
    }
    public void setTitle(String title) {
        this.title = title;
    }

    @Override
    public long getID() {
        return ID;
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
}
