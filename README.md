# 🤖 BeBot — Validador del verbo TO BE

> Chatbot educativo para practicar y validar oraciones afirmativas con el verbo **TO BE** en presente.

---

## ✨ ¿Qué hace?

BeBot analiza una oración en inglés y verifica si utiliza correctamente. Además, identifica errores comunes y muestra una explicación para ayudar al usuario a aprender.

---

## 🚀 Características

| Función | Descripción |
|---|---|
| 🔎 Regex | Valida la estructura de las oraciones |
| 🧠 Diagnóstico | Detecta errores gramaticales comunes |
| 🌎 Filtro de idioma | Rechaza entradas en español |
| 🖥️ GUI | Interfaz gráfica interactiva |
| 💻 CLI | Ejecución desde consola |
| 🧪 Tests | Pruebas automatizadas |
| 📦 Sin dependencias | Solo utiliza Python estándar |

---

## 🛠️ Tecnologías

**Python 3.9+**  
**Regex** · **Tkinter** · **Unittest**

---

## 📂 Estructura

```text
BeBot/
├── src/
│   ├── chatbot_gui.py
│   └── validator.py
├── tests/
├── README.md
└── requirements.txt

---
## ▶️ Uso

| Acción | Comando |
|---|---|
| 🖥️ Interfaz gráfica | `python src/chatbot_gui.py` |
| 🔎 Ejecutar validador | `python src/validator.py` |
| 🧪 Ejecutar pruebas | `python -m unittest discover -s tests` |
