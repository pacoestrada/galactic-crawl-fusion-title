# Galactic Crawl v0.1.0-beta.1

Primera beta pública para descargar e instalar un título de texto en perspectiva con estrellas editables en DaVinci Resolve 21.

**Objetivo de esta versión:** probar el archivo tal como se descarga de GitHub. El `.drfx` y el `.setting` conservan los bytes de la beta local.

## Descarga e instalación

1. En **Assets**, descarga **Galactic-Crawl.drfx**. No necesitas el ZIP de código fuente.
2. Abre Resolve, entra en la página **Fusion** y arrastra el archivo descargado.
3. Confirma la instalación y busca **Galactic Crawl** en **Editar → Biblioteca de efectos → Títulos**.
4. Para la primera prueba, usa 1920 × 1080 y un clip de 60–90 segundos.

También se incluyen una alternativa `.setting`, la guía rápida y `SHA256SUMS.txt`.

## Incluye

- Texto, fuente, tamaño, color, velocidad, perspectiva y recorrido editables.
- Cantidad, brillo, tamaño y distribución de estrellas ajustables.
- Color y opacidad del fondo; opacidad 0 para usar tu propio vídeo o imagen debajo.
- Texto de ejemplo y fuente predeterminada DejaVu Sans Bold, no incluida.

## Estado de las pruebas

Sintaxis Lua, lectura nativa de la tabla, referencias y paquete comprobados. **La instalación, los controles y el render dentro de Resolve siguen pendientes de prueba.** Las vistas del repositorio son simulaciones orientativas, no renders de Fusion.

La beta usa un lienzo de texto fijo y saltos de línea manuales. Si cambias mucho la historia, ajusta tamaño, posición inicial y recorrido.

[Documentación](https://github.com/pacoestrada/galactic-crawl-fusion-title#readme) · [Guía de prueba](https://github.com/pacoestrada/galactic-crawl-fusion-title/blob/main/docs/TESTING.md) · [Comunicar un fallo](https://github.com/pacoestrada/galactic-crawl-fusion-title/issues/new?template=bug_report.yml)
