package ru.goalgomoex.goalgomoex.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import ru.goalgomoex.goalgomoex.entitys.goRole;
import ru.goalgomoex.goalgomoex.entitys.goUserAuthData;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoUserAuth;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoMessage;
import ru.goalgomoex.goalgomoex.repository.GoUserAuthRepository;
import ru.goalgomoex.goalgomoex.utils.exeption.InvalidPasswordException;
import ru.goalgomoex.goalgomoex.utils.exeption.UserAlreadyExistsException;
import ru.goalgomoex.goalgomoex.utils.exeption.UserNotFoundException;

import java.util.HashSet;
import java.util.Optional;

@Service
public class GoUserAuthService implements UserDetailsService {
    @Autowired private GoUserAuthRepository goUserAuthRepository;
    public dtoMessage registerUser(dtoUserAuth dtoUserAuth) throws UserAlreadyExistsException {
        if (goUserAuthRepository.existsByUsername(dtoUserAuth.getEmail())) throw new UserAlreadyExistsException();
        goUserAuthData newUser = new goUserAuthData();
        newUser.setRoles(new goRole("USER","USER"));
        newUser.setUsername(dtoUserAuth.getEmail());
        newUser.setPassword(bCryptPasswordEncode().encode(dtoUserAuth.getPassword()));
        goUserAuthRepository.save(newUser);
        return new dtoMessage("Success", "User registered successfully");
    }
    public boolean deleteUser(Long userId) {
        Optional<goUserAuthData> user = goUserAuthRepository.findById(userId);
        if (user.isPresent()) {
            user.get().setEnabled(false);
            return true;
        }
        return false;
    }
    public dtoMessage loginUser(dtoUserAuth dtoUserAuth) throws InvalidPasswordException, UserNotFoundException {
        goUserAuthData existingUser = goUserAuthRepository.findByUsername(dtoUserAuth.getEmail());
        if (existingUser != null)
            if (bCryptPasswordEncode().matches(dtoUserAuth.getPassword(), existingUser.getPassword()))
                return new dtoMessage("Success", "User " + existingUser.getUsername() + " logged in successfully");
            else throw new InvalidPasswordException();
        else throw new UserNotFoundException(dtoUserAuth.getEmail());
    }
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        return goUserAuthRepository.findByUsername(username);
    }
    @Bean
    public BCryptPasswordEncoder bCryptPasswordEncode() {
        return new BCryptPasswordEncoder();
    }
}
