# Chatbot con expresiones regulares — Verbo *to be*

Este proyecto valida frases sencillas en inglés con el verbo *to be* en presente afirmativo y ofrece retroalimentación ante errores comunes de concordancia.

## Requisitos

Se requiere Python 3.9 o superior. El programa utiliza únicamente la biblioteca estándar, por lo que no es necesario instalar paquetes externos.

## Ejecución

Desde esta carpeta, ejecutar:

```bash
python3 src/chatbot.py
```

Para ejecutar una comprobación rápida del validador:

```bash
python3 src/validator.py
```

Para ejecutar las pruebas:

```bash
python3 -m unittest discover -s tests
```

## Alcance

El validador cubre sujetos pronombres, nombres propios, grupos con `the` y demostrativos; las formas del presente `am`, `are` e `is`; y complementos formados por palabras en inglés. No pretende validar toda la gramática inglesa.

## Estructura

```text
entrega_automatas/
├── src/
│   ├── chatbot.py
│   └── validator.py
├── tests/
│   └── test_validator.py
├── docs/
│   ├── informe.md
│   └── informe.pdf
└── README.md
```
