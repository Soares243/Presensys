package br.unisales.presensys_web_backend.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

import br.unisales.presensys_web_backend.enums.Shift;

@Getter
@Setter
@Entity
@Table(name = "Users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "name_user", nullable = false)    
    private String nome;

    @Column(name = "enrollment_user", nullable = false, unique = true)
    private String enrollment;

    @Enumerated(EnumType.STRING)
    @Column(name = "shift_user", nullable = false)
    private Shift shift;

    @Column(name = "password_user", nullable = false)
    private String password;

    @Column(name = "class_user", nullable = false)
    private String turma;

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Biometrics> biometrics;

    // getters and setters

}
