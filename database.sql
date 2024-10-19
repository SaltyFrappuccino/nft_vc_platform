SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema nft_vc_platform
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `nft_vc_platform` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `nft_vc_platform` ;

-- -----------------------------------------------------
-- Table `nft_vc_platform`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nft_vc_platform`.`users` ;

CREATE TABLE IF NOT EXISTS `nft_vc_platform`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(100) NULL DEFAULT NULL,
  `last_name` VARCHAR(100) NULL DEFAULT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `bio` TEXT NULL DEFAULT NULL,
  `skills` JSON NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE UNIQUE INDEX `email` ON `nft_vc_platform`.`users` (`email` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `nft_vc_platform`.`certificates`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nft_vc_platform`.`certificates` ;

CREATE TABLE IF NOT EXISTS `nft_vc_platform`.`certificates` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `issuer` VARCHAR(255) NOT NULL,
  `issued_date` DATE NOT NULL,
  `type` ENUM('VC', 'NFT') NULL DEFAULT 'VC',
  `owner_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `certificates_ibfk_1`
    FOREIGN KEY (`owner_id`)
    REFERENCES `nft_vc_platform`.`users` (`id`)
    ON DELETE SET NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `owner_id` ON `nft_vc_platform`.`certificates` (`owner_id` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `nft_vc_platform`.`companies`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nft_vc_platform`.`companies` ;

CREATE TABLE IF NOT EXISTS `nft_vc_platform`.`companies` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `address` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE UNIQUE INDEX `name` ON `nft_vc_platform`.`companies` (`name` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `nft_vc_platform`.`company_employees`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nft_vc_platform`.`company_employees` ;

CREATE TABLE IF NOT EXISTS `nft_vc_platform`.`company_employees` (
  `company_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`company_id`, `user_id`),
  CONSTRAINT `company_employees_ibfk_1`
    FOREIGN KEY (`company_id`)
    REFERENCES `nft_vc_platform`.`companies` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `company_employees_ibfk_2`
    FOREIGN KEY (`user_id`)
    REFERENCES `nft_vc_platform`.`users` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE INDEX `user_id` ON `nft_vc_platform`.`company_employees` (`user_id` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `nft_vc_platform`.`nft_tokens`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nft_vc_platform`.`nft_tokens` ;

CREATE TABLE IF NOT EXISTS `nft_vc_platform`.`nft_tokens` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `certificate_id` INT NULL DEFAULT NULL,
  `token_hash` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `nft_tokens_ibfk_1`
    FOREIGN KEY (`certificate_id`)
    REFERENCES `nft_vc_platform`.`certificates` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

CREATE UNIQUE INDEX `token_hash` ON `nft_vc_platform`.`nft_tokens` (`token_hash` ASC) VISIBLE;

CREATE INDEX `certificate_id` ON `nft_vc_platform`.`nft_tokens` (`certificate_id` ASC) VISIBLE;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
