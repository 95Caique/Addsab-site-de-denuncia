from enum import Enum

ABANDONO = 'ABANDONO'
MAUS_TRATOS = 'MAUS_TRATOS'
NEGLIGENCIA = 'NEGLIGENCIA'

tipo_maus_tratos_choices = [
    ("Abandono", "Abandono"),
    ("Negligencia", "Negligência"),
    ("Violencia Fisica", "Violencia Fisica"),
    ("Trabalho Forçado", "Trabalho Forçado"),
    ("Alimentacao Inadequada", "Alimentação Inadequada"),
    ("Outros", "Outros"),
]