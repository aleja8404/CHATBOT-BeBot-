"""Validador de frases en inglés con el verbo TO BE.

El alcance se limita a estructuras simples de sujeto + to be + complemento,
solo en presente afirmativo.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Pattern


# Fragmentos léxicos permitidos por la especificación del proyecto.
# El complemento NO debe comenzar con 'not' ni contener contracciones negativas.
# Incluye dígitos (0-9) para permitir la expresión de la edad (ej: "24 years old").
COMPLEMENT = r"(?!not\b|n't\b)[A-Za-z0-9]+(?:[ -](?!not\b|n't\b)[A-Za-z0-9]+)*"

# Pronombres que no deben ser interpretados como nombres propios.
_PRONOUNS = r"(?:I|you|he|she|it|we|they|this|that|these|those)"

# Nombre propio: empieza por mayúscula y no es un pronombre.
_PROPER_NAME = rf"(?!(?:{_PRONOUNS})\b)[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*"

# Sujetos: pronombres personales, nombres propios, grupos con The y demostrativos.
SUBJECT = (
    rf"(?:{_PRONOUNS}|"
    rf"the\s+[A-Za-z]+(?:\s+[A-Za-z]+)*|"
    rf"(?:this|that|these|those)\s+[A-Za-z]+(?:\s+[A-Za-z]+)*|"
    rf"{_PROPER_NAME})"
)

# Patrón explícito: presente afirmativo únicamente.
PATTERNS: dict[str, Pattern[str]] = {
    "present affirmative": re.compile(
        rf"^(?:I\s+am|you\s+are|we\s+are|they\s+are|"
        rf"(?:he|she|it)\s+is|(?:this|that)\s+is|"
        rf"(?:these|those)\s+are|the\s+[A-Za-z]+(?:\s+[A-Za-z]+)*\s+(?:is|are)|"
        rf"{_PROPER_NAME}\s+is)\s+{COMPLEMENT}$",
        re.IGNORECASE,
    ),
}


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    category: str
    message: str
    normalized: str


def normalize(sentence: str) -> str:
    """Limpia espacios y signos finales sin modificar el contenido esencial."""
    cleaned = re.sub(r"\s+", " ", sentence.strip())
    return cleaned.rstrip(".!?").strip()


def _common_error(sentence: str) -> str:
    """Provides pedagogical feedback in English for common errors."""
    lower = sentence.lower()
    if re.search(r"\bnot\b|n't\b", lower):
        return "Only affirmative sentences are allowed (no 'not' or negative contractions)."
    if re.search(r"\b(?:was|were)\b", lower):
        return "Only present tense sentences are allowed (use am, is, or are, not past tense)."
    if sentence.strip().endswith("?") or lower.startswith(("am ", "is ", "are ")):
        return "Only affirmative present tense sentences are allowed, not questions."
    if re.search(r"\bi\s+is\b", lower):
        return "Check subject-verb agreement: use 'am' with 'I', not 'is'."
    if re.search(r"\b(?:i|he|she|it|this|that|the\s+\w+)\s+are\b", lower):
        return "Check subject-verb agreement: use 'am' or 'is' with singular subjects in present tense, not 'are'."
    if re.search(r"\b(?:you|we|they|these|those)\s+is\b", lower):
        return "Check subject-verb agreement: use 'are' with plural subjects, not 'is'."
    if re.search(r"\b(?:am|is|are)\b", lower) is None:
        return "The sentence must include an affirmative present form of the verb TO BE: am, is, or are."
    return "Unrecognized sentence structure. Remember to use the pattern: Subject + am/is/are + complement."


_SPANISH_WORDS = {
    "yo", "tú", "tu", "él", "ella", "ellas", "ellos", "nosotros", "nosotras",
    "usted", "ustedes", "mí", "mis", "nuestro", "nuestra", "nuestros", "nuestras",
    "este", "esta", "estos", "estas", "ese", "esa", "esos", "esas", "aquel",
    "aquella", "aquellos", "aquellas", "las", "un", "una", "unos", "unas",
    "del", "al", "con", "para", "como", "pero", "porque", "sí",
    "soy", "eres", "somos", "sois", "éramos", "eran", "estoy", "estás",
    "está", "estamos", "estáis", "están", "estaba", "estabas", "estábamos",
    "estaban", "tengo", "tienes", "tiene", "tenemos", "tienen", "hace", "hacen",
    "lloviendo", "llueve", "comiendo", "trabajando", "estudiando", "hablando",
    "jugando", "viendo", "corriendo", "haciendo", "estudiante", "estudiantes",
    "profesor", "profesora", "profesores", "profesoras", "maestro", "maestra",
    "doctora", "niño", "niña", "niños", "niñas", "hijo", "hija", "padre", "madre",
    "hermano", "hermana", "amigo", "amiga", "amigos", "amigas", "casa", "escuela",
    "colegio", "universidad", "trabajo", "ciudad", "pueblo", "pais", "país",
    "perro", "perros", "gato", "gatos", "bonito", "bonita", "bonitos", "bonitas",
    "bueno", "buena", "buenos", "buenas", "malo", "mala", "malos", "malas",
    "grande", "grandes", "pequeño", "pequeña", "pequeños", "pequeñas", "feliz",
    "felices", "triste", "tristes", "cansado", "cansada", "cansados", "cansadas",
    "enfermo", "enferma", "enfermos", "enfermas", "alto", "alta", "altos", "altas",
    "bajo", "baja", "bajos", "bajas", "nuevo", "nueva", "nuevos", "nuevas",
    "viejo", "vieja", "viejos", "viejas", "hermoso", "hermosa", "lindo", "linda",
    "inteligente", "inteligentes", "cartagena", "bogota", "bogotá", "medellin",
    "medellín", "cali", "barranquilla", "colombia", "español", "espanol",
    "inglés", "gracias", "hola", "buenos", "dias", "días", "tardes", "noches",
}


def _detect_spanish(sentence: str) -> str | None:
    """Detects Spanish words or characters and returns an error message if found."""
    if re.search(r"[áéíóúñÁÉÍÓÚÑ¿¡]", sentence):
        return "Spanish is not allowed. Please enter your sentence in English using the verb TO BE."

    words = re.findall(r"\b[A-Za-z]+\b", sentence.lower())
    detected_spanish = [w for w in words if w in _SPANISH_WORDS]
    if detected_spanish:
        example = detected_spanish[0]
        return f"Spanish word detected ('{example}'). Spanish is not allowed. Please write your sentence in English."

    return None


def validate(sentence: str) -> ValidationResult:
    """Validates an English sentence and classifies its grammatical structure."""
    normalized = normalize(sentence)
    if not normalized:
        return ValidationResult(False, "invalid", "The input is empty.", normalized)

    spanish_err = _detect_spanish(sentence)
    if spanish_err:
        return ValidationResult(False, "invalid", spanish_err, normalized)

    for category, pattern in PATTERNS.items():
        if pattern.fullmatch(normalized):
            return ValidationResult(
                True,
                category,
                f"Correct sentence in {category}.",
                normalized,
            )

    return ValidationResult(False, "invalid", _common_error(normalized), normalized)


_INVALID_NAME_WORDS = {
    "a", "an", "the", "yes", "no", "si", "sí", "hello", "hi", "hey", "hola",
    "me", "llamo", "mi", "nombre", "es", "soy", "esta", "está", "en",
    "student", "teacher", "doctor", "boy", "girl", "cat", "dog", "man", "woman",
    "happy", "sad", "good", "bad", "fine", "old", "young", "tired", "sick",
}


def extract_valid_name(text: str) -> str | None:
    """Extracts and validates if the input corresponds to a proper name in English."""
    cleaned = text.strip().rstrip(".!?")
    if not cleaned:
        return None

    # Pattern 1: "My name is <Name>" / "My name's <Name>"
    m_my_name = re.match(
        r"^(?:my\s+name\s+(?:is|'s))\s+([A-Za-z]+(?:\s+[A-Za-z]+)*)$",
        cleaned,
        re.IGNORECASE,
    )
    if m_my_name:
        candidate = m_my_name.group(1).strip()
        if _is_valid_name_str(candidate):
            return candidate.title()

    # Pattern 2: "I am <Name>" / "I'm <Name>"
    m_i_am = re.match(
        r"^(?:I\s+am|I'm)\s+([A-Za-z]+(?:\s+[A-Za-z]+)*)$",
        cleaned,
        re.IGNORECASE,
    )
    if m_i_am:
        candidate = m_i_am.group(1).strip()
        if _is_valid_name_str(candidate):
            return candidate.title()

    # Pattern 3: Direct name (e.g. "Carlos", "Sofia")
    if _is_valid_name_str(cleaned):
        return cleaned.title()

    return None


def _is_valid_name_str(name_str: str) -> bool:
    name_clean = name_str.strip()
    words = name_clean.split()
    if not (1 <= len(words) <= 3):
        return False

    for w in words:
        if not re.match(r"^[A-Za-z]+$", w):
            return False
        if w.lower() in _INVALID_NAME_WORDS:
            return False

    lower = name_clean.lower()
    sentence_starters = (
        "he is", "she is", "it is", "they are", "we are", "you are",
        "this is", "that is", "there is", "who is", "what is", "how are", "i am", "i'm"
    )
    for starter in sentence_starters:
        if lower.startswith(starter):
            return False

    return True


if __name__ == "__main__":
    examples = [
        "I am a teacher",
        "She is happy",
        "They are students",
        "I is student",
        "He was at home",
        "I am not tired",
    ]
    for example in examples:
        print(example, "->", validate(example))
