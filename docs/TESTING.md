# Prueba desde GitHub hasta DaVinci

Esta guía prueba **v0.1.0-beta.1 descargada de GitHub**, para distinguir fallos de distribución de fallos dentro del editor. No es un informe de resultados: las casillas son pasos pendientes de ejecución manual.

## 1. Descargar

- [ ] Abrir [la versión beta](https://github.com/pacoestrada/galactic-crawl-fusion-title/releases/tag/v0.1.0-beta.1).
- [ ] En **Assets**, descargar `Galactic-Crawl.drfx` a una carpeta nueva.
- [ ] Comprobar que el archivo conserva la extensión `.drfx` y no termina en `.html`, `.txt` o `.zip`.
- [ ] Opcional: descargar `SHA256SUMS.txt` a la misma carpeta y comprobar la suma del `.drfx`.

En Linux, desde esa carpeta:

```sh
sha256sum Galactic-Crawl.drfx
```

Compara el resultado con la línea de `Galactic-Crawl.drfx` en `SHA256SUMS.txt`. Si descargas los tres archivos listados, puedes ejecutar `sha256sum -c SHA256SUMS.txt`.

Una coincidencia SHA-256 confirma que tienes el mismo archivo publicado; no confirma que Fusion lo renderice correctamente.

## 2. Instalar sin confundirlo con una copia local

- [ ] Si instalaste antes el título local, retira esa copia desde su carpeta de instalación; conserva cualquier modificación propia. Reinicia Resolve.
- [ ] Arrastrar **el archivo recién descargado** a la página Fusion de un proyecto.
- [ ] Confirmar que aparece el diálogo de instalación y completar la instalación.
- [ ] Buscar **Galactic Crawl** en la biblioteca de títulos. Reiniciar Resolve si no aparece.
- [ ] Arrastrar el título a una línea de tiempo 1920 × 1080 y darle 60–90 segundos.

## 3. Reproducir y editar

- [ ] Ver estrellas de fondo y texto que entra por abajo, asciende y se estrecha hacia el horizonte.
- [ ] Revisar un fotograma al 10 %, 25 %, 50 %, 75 % y al final del clip; comprobar que el texto no queda invertido ni cortado de forma inesperada.
- [ ] Sustituir una frase y comprobar que cambia en pantalla.
- [ ] Cambiar tamaño y color de texto; probar otra fuente instalada si no aparece.
- [ ] Cambiar la velocidad y alargar el clip; comprobar que el desplazamiento responde.
- [ ] Cambiar horizonte, perspectiva y ancho; restaurar los valores iniciales al terminar.
- [ ] Cambiar cantidad, brillo, tamaño y distribución de estrellas.
- [ ] Cambiar el color del espacio.
- [ ] Poner una imagen o vídeo debajo; establecer **Opacidad del fondo = 0** y comprobar que se ve el contenido inferior y permanece el texto.
- [ ] Probar opacidad de fondo 0,5 y 1.
- [ ] Confirmar que al final desaparece el texto y permanece el fondo configurado.
- [ ] Exportar una prueba corta y revisar el archivo exportado, además de la reproducción en la línea de tiempo.

No se incluyen créditos, música ni audio. La vista orientativa del repositorio no debe usarse como evidencia de que el render real ya está validado.

## Si algo falla

| Síntoma | Primera comprobación |
| --- | --- |
| El enlace no descarga o da 404 | Anota el enlace exacto y comprueba que estás en la etiqueta `v0.1.0-beta.1`. |
| Se descarga HTML o una página | Usa el asset `.drfx`, no «Guardar página como» ni el ZIP del repositorio. |
| La suma no coincide | Descarga de nuevo el asset en otra carpeta y compara con el manifiesto de esa misma versión. |
| No hay diálogo de instalación | Comprueba la extensión y arrastra el archivo a Fusion; el doble clic depende de la asociación del sistema. |
| El título no aparece | Reinicia Resolve; revisa la carpeta `Templates/Edit/Titles` y que no haya copias duplicadas. |
| Hay estrellas pero no texto | Prueba al 10–25 % del clip, comprueba la fuente instalada y restaura los valores iniciales. |
| El texto se corta | Reduce tamaño, acorta las líneas o revisa la longitud total. No hay ajuste automático de líneas. |
| Pantalla negra, errores o lentitud | Anota fotograma, resolución, fps y mensaje; adjunta captura del Inspector y de los nodos en Fusion. |

Crea una [incidencia](https://github.com/pacoestrada/galactic-crawl-fusion-title/issues/new?template=bug_report.yml) con versión/build de Resolve, Free/Studio, sistema operativo, resolución/fps, versión descargada, paso que falla y resultado esperado/observado. Distingue entre «fallo de descarga», «instalación» y «render/controles».
