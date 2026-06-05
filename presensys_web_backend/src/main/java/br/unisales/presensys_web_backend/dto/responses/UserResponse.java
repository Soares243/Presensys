package br.unisales.presensys_web_backend.dto.responses;

import br.unisales.presensys_web_backend.enums.Shift;
import lombok.Data;

@Data
public class UserResponse {

    private Long id;
    private String name;
    private String enrollment;
    private Shift shift;
    private String className;
}
