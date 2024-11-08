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
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    sobrenome VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    data_nascimento DATE,
    genero ENUM('Masculino', 'Feminino', 'Outro'),
    telefone VARCHAR(20),
    endereco VARCHAR(255)
);

-- Tabela Informacoes_Medicas
CREATE TABLE Informacoes_Medicas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    tipo_sanguineo ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-') NOT NULL,
    comorbidades TEXT,          
    alergias TEXT,              
    medicamentos TEXT,          
    historico_familiar TEXT,    
    observacoes TEXT,           
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id) ON DELETE CASCADE
);


-- Tabela Pets
CREATE TABLE Pets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    especie ENUM('cachorro', 'gato', 'pássaro', 'réptil', 'outro') NOT NULL,
    raca VARCHAR(100),
    data_nascimento DATE,
    sexo ENUM('M', 'F'),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
);

-- Tabela Informacoes_Medicas_Pets
CREATE TABLE Informacoes_Medicas_Pets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_pet INT NOT NULL,
    tipo_sanguineo ENUM('A', 'B', 'AB', 'O') DEFAULT NULL,
    alergias TEXT,               -- Descrição de alergias
    doencas_cronicas TEXT,       -- Doenças crônicas do pet
    medicamentos TEXT,           -- Lista de medicamentos em uso
    historico_vacinas TEXT,      -- Histórico de vacinas
    observacoes TEXT,            -- Campo para anotações adicionais
    FOREIGN KEY (id_pet) REFERENCES Pets(id) ON DELETE CASCADE
);
