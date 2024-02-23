package ru.goalgomoex.goalgomoex.controllers.api.v1;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoUserAuth;
import ru.goalgomoex.goalgomoex.entitys.dto.dtoMessage;
import ru.goalgomoex.goalgomoex.services.GoUserAuthService;
import ru.goalgomoex.goalgomoex.utils.exeption.InvalidPasswordException;
import ru.goalgomoex.goalgomoex.utils.exeption.UserAlreadyExistsException;
import ru.goalgomoex.goalgomoex.utils.exeption.UserNotFoundException;

@RestController
@RequestMapping("/api/v1/auth/")
public class RestAuthController {
    @Autowired private GoUserAuthService goUserAuthService;
    @PostMapping("/register")
    public ResponseEntity<dtoMessage> registerUser(@RequestBody dtoUserAuth dtoUserAuth) {
        try {
            dtoMessage responseMessage = goUserAuthService.registerUser(dtoUserAuth);
            return ResponseEntity.status(HttpStatus.CREATED).body(responseMessage);
        } catch (UserAlreadyExistsException e) {
            return ResponseEntity.status(HttpStatus.CONFLICT).body(new dtoMessage("Error", "User with username " + dtoUserAuth.getEmail() + " already exists."));
        }
    }
    @PostMapping("/login")
    public ResponseEntity<dtoMessage> loginUser(@RequestBody dtoUserAuth dtoUserAuth) {
        try {
            dtoMessage responseMessage = goUserAuthService.loginUser(dtoUserAuth);
            return ResponseEntity.ok(responseMessage);
        } catch (InvalidPasswordException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(new dtoMessage("Error", "Invalid password."));
        } catch (UserNotFoundException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new dtoMessage("Error", "User not found with username: " + dtoUserAuth.getEmail()));
        }
    }
    @PostMapping("/test-request")
    public ResponseEntity<String> testPostRequest() {
        return ResponseEntity.ok("POST request successful");
    }
}
