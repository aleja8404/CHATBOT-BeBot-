BeBot 🤖 - Chatbot Validador del Verbo TO BE

BeBot es un chatbot educativo e interactivo desarrollado en Python que valida oraciones afirmativas en tiempo presente utilizando el verbo TO BE (am, is, are) mediante Expresiones Regulares (Regex).

El sistema analiza la estructura gramatical de la entrada del usuario, detecta errores de concordancia y proporciona retroalimentación pedagógica si la frase incluye negaciones, pasados, preguntas o texto en español.

🚀 Características Principales

Validación mediante Regex: Coincidencia sintáctica estricta para oraciones afirmativas en presente (I am, He/She/It is, You/We/They are).

Diagnóstico Heurístico de Errores: Explicaciones pedagógicas detalladas cuando una frase es rechazada (ej. detección de pasados was/were, negaciones not/n't, preguntas o errores de concordancia como "She are").

Filtro de Idioma: Detecta y rechaza oraciones ingresadas en español mediante análisis ortográfico y léxico.

Interfaces Disponibles: Modo consola (CLI) e interfaz gráfica de usuario (GUI).

Sin Dependencias Externas: Funciona al 100% con la biblioteca estándar de Python 3.9+.

💻 Ejecución
Modo Interfaz Gráfica (GUI):
python src/chatbot_gui.py

Probar el Validador Directamente:
python src/validator.py

🧪 Pruebas Automatizadas:
Para ejecutar la suite de pruebas unitarias: python -m unittest discover -s tests
