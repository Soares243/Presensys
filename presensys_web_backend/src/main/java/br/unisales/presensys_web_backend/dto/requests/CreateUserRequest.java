package br.unisales.presensys_web_backend.dto.requests;

import br.unisales.presensys_web_backend.enums.Shift;
import lombok.Data;

@Data
public class CreateUserRequest {

    private String name;
    private String enrollment;
    private Shift shift;
    private String password;
    private String className;
}
