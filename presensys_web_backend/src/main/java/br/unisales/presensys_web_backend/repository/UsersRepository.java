package br.unisales.presensys_web_backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import br.unisales.presensys_web_backend.entity.User;

import java.util.Optional;

public interface UsersRepository extends JpaRepository<User, Long> {
    Optional<User> findByEnrollment(String enrollment);

    boolean existsByEnrollment(String enrollment);
}
