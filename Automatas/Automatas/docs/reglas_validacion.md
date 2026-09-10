# Reglas de Validación del Verbo *TO BE* (BeBot)

Este documento detalla las reglas gramaticales, estructuras sintácticas y expresiones regulares utilizadas por el módulo `validator.py` para analizar y clasificar las oraciones en inglés introducidas por el usuario.

---

## 1. Etapa de Normalización (`normalize`)

Antes de evaluar cualquier regla o patrón, la oración ingresada por el usuario pasa por un proceso de limpieza inicial:
- **Espacios en blanco**: Se remueven espacios al inicio y final, y se reducen secuencias de múltiples espacios consecutivos a un único espacio (`\s+` $\rightarrow$ `" "`).
- **Signos de puntuación finales**: Se eliminan del final de la frase los signos `.`, `!`, `?` (`rstrip(".!?")`), lo que permite validar oraciones afirmativas, negativas e interrogativas sin interferencia por la puntuación final.

---

## 2. Componentes Léxicos Básicos

Las reglas de validación se construyen de forma modular combinando las siguientes entidades:

### A. Complemento (`COMPLEMENT`)
```regex
(?!not\b|n't\b)[A-Za-z0-9]+(?:[ -](?!not\b|n't\b)[A-Za-z0-9]+)*
```
- **Definición**: Cadena compuesta por palabras alfabéticas o números (`[A-Za-z0-9]+`), separados opcionalmente por espacios o guiones.
- **Soporte de Edad**: Permite números como `"24"`, `"10"`, `"1"` seguidos de expresiones como `"years old"` o `"year old"`.
- **Restricción de Lookahead Negativo (`(?!not\b|n't\b)`)**: Evita que el complemento comience con la palabra `not` o contracciones negativas como `n't`, garantizando la separación correcta entre el operador negativo de la oración y su complemento.

### B. Pronombres (`_PRONOUNS`)
```regex
(?:I|you|he|she|it|we|they|this|that|these|those)
```
Comprende pronombres personales y demostrativos en inglés.

### C. Nombres Propios (`_PROPER_NAME`)
```regex
(?!(?:I|you|he|she|it|we|they|this|that|these|those)\b)[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*
```
Reconoce palabras que inician con mayúscula (como `"Maria"` o `"John Smith"`), asegurando mediante un lookahead negativo que pronombres como `"I"` no sean clasificados erróneamente como nombres propios.

---

## 3. Matriz de Patrones Sintácticos (`PATTERNS`)

El validador evalúa únicamente la categoría gramatical de **Presente Afirmativo** mediante una expresión regular exacta (`fullmatch` en modo insensible a mayúsculas):

### Presente Afirmativo (`presente afirmativo`)
- **Fórmula**: `[Sujeto] + [am | is | are] + [Complemento]`
- **Reglas de Concordancia**:
  - `I` $\rightarrow$ `am`
  - `he` | `she` | `it` | `this` | `that` | `_PROPER_NAME` $\rightarrow$ `is`
  - `you` | `we` | `they` | `these` | `those` $\rightarrow$ `are`
  - `the <sustantivo>` $\rightarrow$ `is` / `are`
- **Ejemplos válidos**: `"I am a teacher"`, `"The cat is brown"`, `"He is 24 years old"`.

> [!NOTE]
> Oraciones en formas negativas, interrogativas o en tiempo pasado son marcadas como inválidas (`valid = False`).

---

## 4. Sistema de Diagnóstico de Errores (`_common_error`)

Cuando una oración no coincide con el patrón afirmativo en presente (`valid = False`), la función `_common_error` ejecuta verificaciones heurísticas para devolver retroalimentación pedagógica precisa:

1. **Uso de Formas Negativas**: Si detecta `not` o contracciones como `n't`, notifica que solo se aceptan oraciones afirmativas.
2. **Uso de Pasado**: Si detecta `was` o `were`, recuerda usar únicamente el tiempo presente (`am`, `is`, `are`).
3. **Estructura Interrogativa**: Si detecta inicio con verbo o signo `?`, notifica que no se aceptan preguntas.
4. **Error de concordancia en `I`**: Detecta expresiones como `"I is"` y sugiere usar `am`.
5. **Error de concordancia en Sujeto Singular**: Detecta pronombres o sustantivos singulares acompañados de `"are"` (ej. `"She are"`) y sugiere utilizar `am` o `is`.
6. **Error de concordancia en Sujeto Plural**: Detecta pronombres plurales acompañados de `"is"` (ej. `"They is"`) y sugiere utilizar `are`.
7. **Ausencia del verbo TO BE**: Si la oración no contiene `am`, `is` o `are`, notifica al usuario que debe incluir una forma afirmativa en presente del verbo *TO BE*.
8. **Estructura no reconocida**: Mensaje genérico de ayuda con el patrón básico.
