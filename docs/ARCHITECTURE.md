# Arquitectura

`Galactic Crawl.setting` contiene un `GroupOperator` llamado `GalacticCrawl`, con siete nodos y 23 componentes `InstanceInput` publicados. Los componentes RGB/RGBA y la pareja fuente/estilo se agrupan en controles del Inspector; 23 no significa 23 selectores visuales independientes.

```text
Canvas ─────────────┐
Story (TextPlus) ────┴─ Crawl (Custom) ── máscara ── Ink (Background) ──┐
Space (Background) ──── Stars (Custom) ────────────────────────────────┴─ Final (Merge)
```

## Texto y perspectiva

`Story` compone texto blanco sobre transparencia en un lienzo fijo de 1920 × 4096, sin heredar el formato de fotograma de la composición. `Canvas`, `Space` e `Ink` sí solicitan el formato de la composición, con 1920 × 1080 guardado como referencia.

`Crawl` toma `Canvas` como primera imagen para establecer el lienzo de salida y `Story` como segunda imagen. Un mapeo proyectivo inverso obtiene las coordenadas de muestreo del texto; `geta2b` lee la máscara y devuelve cero fuera de la imagen.

El progreso se calcula con `(time - comp.RenderStart) / max(1, comp.RenderEnd - comp.RenderStart)`, limitado al intervalo 0–1. La velocidad y el recorrido multiplican ese progreso. Hay una atenuación espacial cerca del horizonte y otra temporal durante el último 8 % del clip. Los divisores tienen mínimos para evitar singularidades.

No se usa una cámara 3D ni un nodo de texto extruido: la perspectiva se calcula sobre la máscara 2D. El comportamiento real de muestreo, suavizado y texto queda pendiente de revisión dentro de Resolve.

## Estrellas y transparencia

`Stars` usa una cuadrícula de 96 × 54 con posiciones desplazadas por funciones deterministas de la semilla. Cada celda puede contener un punto de brillo y tamaño variables. El campo permanece estático si los controles no se animan.

`Space` suministra el color base. La opacidad del fondo multiplica tanto RGB como alfa en `Stars`, conservando una salida premultiplicada. `Final` compone `Ink` encima del fondo. Ocultar el fondo no atenúa el texto.

La cuadrícula y la escala de los puntos se diseñaron para formato horizontal 16:9. Otros formatos no se declaran validados.

## Paquete y archivos

El `.drfx` de esta beta contiene exactamente:

```text
Edit/Titles/Galactic Crawl.setting
```

No incluye miniaturas de biblioteca, fuentes, fuses, plugins o medios externos. Las vistas orientativas de `docs/` no forman parte del instalador.

`src/Galactic Crawl.setting`, `dist/Galactic-Crawl.setting` y el miembro interno del `.drfx` deben coincidir byte a byte. El nombre del archivo descargable usa guiones para dar URLs sencillas; el título interno conserva espacios.

Esta publicación conserva el `.drfx` original sin reempaquetarlo. En futuras versiones puede generarse un ZIP con ese único miembro y extensión `.drfx`; los metadatos del ZIP pueden cambiar su SHA-256 aunque el `.setting` sea idéntico. Actualiza entonces `dist/SHA256SUMS.txt`, el historial, la etiqueta y las notas de versión conjuntamente.

## Referencias

Funciones de `Custom`, coordenadas, evaluación intermedia y muestreo: manual de DaVinci Resolve instalado, sección **Custom Tool / Miscellaneous Nodes**. Los manuales se obtienen en el [centro oficial de Blackmagic Design](https://www.blackmagicdesign.com/support/family/davinci-resolve-and-fusion).
