# Proyecto: Sistema Lógico para la Asignación de Horarios Académicos

Este repositorio contiene el desarrollo del proyecto para la asignatura de Lógica para Ciencias de la Computación de la Universidad del Rosario.

El objetivo principal es modelar el problema de asignación de horarios académicos mediante lógica proposicional, transformando las restricciones institucionales en una base de conocimiento (cláusulas) que pueda ser resuelta por un SAT Solver para encontrar un horario válido y libre de conflictos.

## Integrantes
- Jhonatan Gutiérrez Rondón
- Juan Andrés Pineda

## Estructura del Repositorio
- `Horarios-checkpoint.py`: Script principal que define los dominios (cursos, profesores, horarios, salones) y ejecuta el modelo SAT.
- `Logica-checkpoint.py`: Módulo base provisto para la lógica del SAT Solver y Tableaux.
- `docs/`: Directorio que contiene los documentos formales de las entregas (PDF y/o código fuente LaTeX).

## Entregas
- [Entrega 1](./Entregas/primera_entraga_logica_computacion.pdf): Modelado formal y base de conocimiento inicial.
- [Entrega 2](./Entregas/segunda_entrega_logica_computación-2.pdf): Simbolización de las reglas del problema (Y-torias y O-torias).

## Entorno de Ejecución y Dependencias
El proyecto está desarrollado en Python. Para ejecutar el script principal, asegúrese de tener instalado Python 3.x y las librerías necesarias:

```bash
pip install matplotlib