# Validación

## Confirmación del usuario y release v0.1.0

El 2026-09-08, el usuario confirmó que el título descargado de GitHub era funcional en varios aspectos comprobados y pidió publicarlo como release. No detalló qué controles verificó. El `.drfx` y el `.setting` de v0.1.0 conservan exactamente los bytes de v0.1.0-beta.1.

Esta confirmación respalda la descarga y el uso observado por el usuario; no constituye una prueba exhaustiva de todos los controles, exportación, rendimiento o compatibilidad.

## Registro técnico original de v0.1.0-beta.1

Fecha de preparación: **2026-09-08**. Entorno local: Linux, con el intérprete instalado de Fusion/Resolve en `/opt/resolve/libs/Fusion/fuscript`.

## Comprobación nativa de lectura

Ejecutada antes de publicar:

1. `loadstring` acepta el `.setting` como expresión de tabla Lua.
2. `bmd.readfile` carga la tabla Fusion.
3. Existen `GalacticCrawl`, su salida y los siete nodos internos.
4. Las referencias publicadas apuntan a nodos presentes.
5. El texto mantiene su lienzo independiente de 1920 × 4096.

Se puede repetir con:

```sh
/opt/resolve/libs/Fusion/fuscript -l lua tools/validate_native.lua 'src/Galactic Crawl.setting'
```

El intérprete puede emitir una advertencia sobre `python2` antes de ejecutar Lua. El resultado relevante es la línea explícita `OK: native Fusion ...`; no basta con el código de salida, porque ese ejecutable puede devolver cero tras un error de Lua.

**Esta comprobación lee una tabla de ajustes. No instancia ni renderiza los nodos en una composición abierta.**

## Comprobación portable

`python3 tools/validate_release.py` utiliza el parser de Lua 5.4 con constructores de tabla sustitutos y comprueba:

- Sintaxis Lua y evaluación de la estructura del `.setting`.
- Tipos y referencias del grafo, ausencia de ciclos y controles publicados.
- El miembro esperado dentro del `.drfx`, sin duplicados ni archivos adicionales.
- Integridad ZIP y coincidencia byte a byte con ambos `.setting`.
- Las sumas SHA-256 de los tres archivos distribuibles.
- Resolución de enlaces Markdown locales de la documentación.

GitHub Actions ejecuta estas mismas comprobaciones en cada push y pull request. El parser portable no comprueba que cada parámetro sea reconocido por Resolve ni evalúa las expresiones de imagen de `Custom`.

## Prueba de distribución

Después de publicar se descargan los tres assets y el manifiesto desde la versión de GitHub a una carpeta independiente. Se comparan con los originales y se comprueba el ZIP descargado. El resultado de esa comprobación corresponde a la distribución de archivos, no a la instalación en Resolve.

## Pendiente de prueba manual

- Descarga mediante navegador e instalación del paquete dentro de Resolve.
- Visibilidad del título y reconocimiento de los controles del Inspector.
- Fuente, saltos de línea, suavizado y composición del texto real.
- Animación completa, transparencia y exportación final.
- Velocidad de reproducción y consumo de memoria.
- Resolve Free/Studio, otros sistemas operativos, formatos verticales y otras resoluciones.

Usa [docs/TESTING.md](docs/TESTING.md) para registrar esa prueba. No se debe marcar esta versión como estable ni describirla como «render verificado» solo porque pasen las comprobaciones automáticas.

## Vistas orientativas

El PNG y el MP4 se generaron fuera de Resolve mediante las fórmulas de perspectiva y estrellas. Son referencias de diseño. El rasterizado de texto y el muestreo pueden diferir de Fusion. El MP4 dura 30 segundos y no prescribe la duración recomendada del clip de 60–90 segundos.
