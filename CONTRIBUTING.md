# Contribuir

La prioridad de esta beta es comprobar el flujo descarga → instalación → edición → render en DaVinci Resolve 21.

Para informar de un fallo, abre una incidencia con el formulario de errores y adjunta versión/build de Resolve, Free/Studio, sistema operativo, resolución/fps, versión descargada y pasos mínimos. Indica si falla la descarga, la instalación o el resultado visual.

Para cambios de código:

1. Modifica `src/Galactic Crawl.setting`.
2. Actualiza el instalador de `dist/` y su alternativa `.setting`.
3. Regenera las sumas SHA-256 y actualiza el historial.
4. Ejecuta `python3 tools/validate_release.py` (Python 3.10+, biblioteca compartida Lua 5.4).
5. Si tienes Resolve, añade resultados de instalación y render con el entorno exacto. Diferencia pruebas reales de vistas simuladas.
6. Abre una pull request con el problema, el cambio y la validación realizada.

No presentes una comprobación de sintaxis como una prueba de render. Las contribuciones se distribuyen bajo la licencia MIT del repositorio.
