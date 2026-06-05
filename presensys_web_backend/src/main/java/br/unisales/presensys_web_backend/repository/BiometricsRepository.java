package br.unisales.presensys_web_backend.repository;

import br.unisales.presensys_web_backend.entity.Biometrics;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface BiometricsRepository extends JpaRepository<Biometrics, Long> {

    List<Biometrics> findByUserId(Long userId);
}
