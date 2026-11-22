CREATE TABLE employees (
    id           INTEGER PRIMARY KEY,
    first_name   VARCHAR(50),
    last_name    VARCHAR(50),
    num_years    INTEGER,
    satisfaction DECIMAL(25,5)
);

INSERT INTO employees (id, first_name, last_name, num_years, satisfaction) VALUES
    ( 1, 'James',  'Bradford', 11, 0.95),
    ( 2, 'Alice',  'Adams',     9, 0.79),
    ( 3, 'Sara',   'Nolan',    20, 0.97),
    ( 4, 'Bob',    'Baker',     4, 0.99),
    ( 5, 'Kent',   'Bennett',   6, 0.86),
    ( 6, 'Dan',    'Carter',    2, 0.50),
    ( 7, 'Linda',  'Chen',      5, 0.80),
    ( 8, 'Eva',    'Diaz',      4, 0.80),
    ( 9, 'Tony',   'Beyer',     8, 0.90),
    (10, 'Finn',   'Evans',     5, 0.79999),
    (11, 'Maria',  'Dawson',   12, 0.91),
    (12, 'Gina',   'Garcia',   10, 0.40),
    (13, 'Hank',   'Ibrahim',   1, 0.95),
    (14, 'Omar',   'Fisher',    7, 0.83),
    (15, 'Ivy',    'Jones',     3, 0.85),
    (16, 'Jack',   'Klein',     8, 0.65),
    (17, 'Priya',  'Hughes',    5, 0.88),
    (18, 'Kim',    'Lopez',     0, 0.90),
    (19, 'Leo',    'Moore',    15, 0.70),
    (20, 'Eric',   'Young',     6, 0.81),
    (21, 'Mia',    'Owens',     6, 0.50),
    (22, 'Ned',    'Perez',     4, 0.79),
    (23, 'Olga',   'Quinn',     7, 0.795),
    (24, 'Paul',   'Reed',      5, 0.30);
