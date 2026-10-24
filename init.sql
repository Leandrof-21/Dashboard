CREATE TABLE IF NOT EXISTS vendas(
    id SERIAL PRIMARY KEY,
    cliente VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    valor NUMERIC(10, 2) NOT NULL,
    data_venda DATE NOT NULL DEFAULT CURRENT_DATE
);

INSERT INTO vendas (cliente, categoria, valor, data_venda) VALUES
('Tech Solutions', 'Software', 1500.00, '2026-10-01'),
('Mercado Alfa', 'Hardware', 3200.50, '2026-10-02'),
('Escola Futuro', 'Serviços', 800.00, '2026-10-02'),
('Tech Solutions', 'Hardware', 4500.00, '2026-10-03'),
('Auto Peças Silva', 'Hardware', 1200.00, '2026-10-04'),
('Mercado Alfa', 'Software', 2100.00, '2026-10-05'),
('Consultoria Beta', 'Serviços', 3500.00, '2026-10-06'),
('Escola Futuro', 'Software', 950.00, '2026-10-07'),
('Auto Peças Silva', 'Serviços', 1800.00, '2026-10-08');