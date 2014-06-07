# -*-coding:utf-8 -*
# These constants are here to propose predefined choices in the admin interface

PRODUCT_TYPES = (
    ('driving', 'Conduite en circulation'),
    ('plateau', 'Conduite sur plateau'),
    ('code_exam', 'Examen de code'),
    ('driving_exam', 'Examen de conduite'),
    ('initial_circuit', 'Conduite sur circuit (initial)'),
    ('medium_circuit', 'Conduite sur circuit (intermédiaire)'),
    ('improvement_circuit', 'Conduite sur circuit (perfectionnement)'),
    ('livre_code', 'Livre de code général'),
    ('live_fiches', 'Livre de fiches moto'),
    ('code', 'Code'),
    ('frais_inscription', 'Frais d\'insciption'),
    ('pack', 'Pack'),
    ('divers', 'Divers'),
)

PRODUCT_DEFAULT_LIMITS = (
    ('initial_circuit', 12),
    ('medium_circuit', 12),
    ('improvement_circuit', 5),
    ('code', 3),
)

PRODUCT_CATEGORIES = (
    ('auto', 'Auto'),
    ('moto', 'Moto'),
)

