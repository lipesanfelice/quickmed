-- Tabela Clinica
CREATE TABLE Clinica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(55) NOT NULL,
    descricao TEXT,
    telefone VARCHAR(20),
    email VARCHAR(55),
    endereco VARCHAR(255),
    latitude DECIMAL(10, 8),  -- ajustado para melhor precisão
    longitude DECIMAL(11, 8), -- ajustado para melhor precisão
    tipo ENUM('veterinário', 'médico') NOT NULL,
    avaliacao DECIMAL(3, 2),  -- ajustado para permitir avaliações como 4.5, 3.7, etc.
    CHECK (avaliacao >= 0 AND avaliacao <= 5),  -- limite de 0 a 5 para avaliação
    horario TEXT
);

-- Tabela Servicos
CREATE TABLE Servicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(55) NOT NULL,
    descricao TEXT
);

-- Tabela de Relacionamento Clinica_Servico
CREATE TABLE Clinica_Servico (
    id_clinica INT,
    id_servico INT,
    PRIMARY KEY (id_clinica, id_servico),
    FOREIGN KEY (id_clinica) REFERENCES Clinica(id) ON DELETE CASCADE,
    FOREIGN KEY (id_servico) REFERENCES Servicos(id) ON DELETE CASCADE
);

-- Tabela Usuarios
CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(55) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
);