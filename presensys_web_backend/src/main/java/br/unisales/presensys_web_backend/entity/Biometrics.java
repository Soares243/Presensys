package br.unisales.presensys_web_backend.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

import br.unisales.presensys_web_backend.enums.Type;

@Getter
@Setter
@Entity
@Table(name = "biometria")
public class Biometrics {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Enumerated(EnumType.STRING)
    @Column(name = "type_biometrics", nullable = false)
    private Type type;

    @Column(name = "value_biometrics", nullable = false)
    private String value;

    @Column(name = "timestamp_biometrics", nullable = false)
    private LocalDateTime timestamp;

    @ManyToOne  
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    // getters and setters


}

