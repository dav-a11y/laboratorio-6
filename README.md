# Laboratorio del 3er Corte - Digitales 3

**Autores:** David Díaz, Jhonatan Vargas, David Lopez  
**Fecha:** Noviembre 2025  
**Materia:** Digitales 3  

---

## Introducción

Este laboratorio tiene como objetivo desarrollar aplicaciones en Python que utilicen **procesamiento paralelo mediante hilos** y **mutex** para sincronización, aplicadas a distintos tipos de proyectos:  

1. **Análisis de Sentimientos de textos en paralelo**.  
2. **Juego 2D tipo Mario Bros con multi-salto y enemigos gestionados por hilos**.  
3. **Detección de Gestos de Mano en tiempo real usando MediaPipe**.  

Cada proyecto incluye una interfaz visual interactiva (Streamlit o Pygame) y es **portable** gracias a su empaquetado en contenedores Docker, permitiendo su ejecución segura en cualquier entorno.

---

## Resumen de los Proyectos

### 1. Análisis de Sentimientos
- Permite subir archivos `.txt` con múltiples comentarios.  
- Cada comentario se clasifica como **positivo, negativo o neutro**.  
- Procesamiento paralelo mediante **hilos** y sincronización con `Lock`.  
- Interfaz visual en **Streamlit**.  
- Empaquetado en Docker para portabilidad.

### 2. Juego 2D tipo Mario Bros
- Juego de plataformas con jugador, enemigos y monedas.  
- Movimiento horizontal y **multi-salto** del jugador.  
- Enemigos y monedas gestionados mediante **hilos** con sincronización.  
- Interfaz gráfica con **Pygame**.  
- Contenedor Docker para ejecución portátil.

### 3. Detección de Gestos de Mano
- Captura de video en tiempo real y detección de gestos con **MediaPipe**.  
- Procesamiento concurrente mediante hilos y protección de variables con **mutex**.  
- Interfaz interactiva en **Streamlit**.  
- Contenedor Docker para ejecución en cualquier equipo.  

---

## link del pdf para visualizar el informe del trabajo

[Ver informe PDF](pdf/laboratorio_digitales3_3corte.pdf)

---

## link de video que evidencia el resultado final de la aplicacion 

[Ver video](https://www.youtube.com/watch?v=YsxCivQDVLg)

---

## link del aplicacion para visualizar el analis de emociones en streamlit
- Se presenta solo este desarrollo debido a que la pagina web del punto de vision de para deteccion de gestos con las manos no fue posible debido a librerias que impidieron su implementacion como la que se desarrollo a continuacion

[Ver app](https://laboratorio-6-c3q5kl5kcqrfnsmqkziuqg.streamlit.app/)


