# Proyecto: Sistema Lógico para la Asignación de Horarios Académicos

Este repositorio contiene el desarrollo del proyecto para la asignatura de Lógica para Ciencias de la Computación de la Universidad del Rosario.

El proyecto representa las reglas de asignación de horarios como fórmulas de lógica proposicional. El programa muestra un horario de ejemplo y verifica que cumpla las reglas. También convierte la base de conocimiento a cláusulas mediante la transformación de Tseitin; todavía no busca automáticamente una solución con un SAT solver.

## Integrantes
- Jhonatan Gutiérrez Rondón
- Juan Andrés Pineda

## Archivos principales
- `Horarios.py`: define los cursos, profesores, bloques y salones; construye las reglas, muestra un horario de ejemplo y aplica la transformación de Tseitin.
- `Logica.py`: contiene las estructuras para representar y evaluar fórmulas proposicionales.
- `Solucion_horarios.ipynb`: explica el modelo, muestra el horario y presenta pruebas de las reglas.

## Entregas
- [Entrega 1](./Entregas/primera_entraga_logica_computacion.pdf): Modelado formal y base de conocimiento inicial.
- [Entrega 2](./Entregas/segunda_entrega_logica_computación-2.pdf): Simbolización de las reglas del problema (Y-torias y O-torias).

## Entorno de Ejecución y Dependencias
El proyecto está desarrollado en Python. Para ejecutar el script y ver el horario de ejemplo, instale Matplotlib y ejecute:

```bash
pip install matplotlib
python Horarios.py
```