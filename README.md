# Encuesta Intercensal · CDMX y Nacional

Tablero estático que utiliza **exclusivamente los tabulados de Data_Actualizada.xlsx**. No combina microdatos, estimaciones antiguas ni factores de expansión propios. Solo reutiliza la cartografía del tablero anterior.

## Uso

Abre `index.html` o publica esta carpeta en GitHub Pages. Conserva junto al HTML `dashboard.bundle.js`, `styles.css`, `explorer.css` y `tabulados.css`. No requiere instalación para consultarlo y funciona sin conexión. Los scripts fuente están reunidos en el archivo bundle y las rutas llevan una versión por contenido para evitar mezclas de caché.

Las pestañas **CDMX** y **Nacional** tienen su propio selector de tema:

- CDMX: nacimiento, residencia hace cinco años, población y sexo, educación, ingresos monetarios, vivienda y discapacidad.
- Nacional: población por entidad, educación, ingresos monetarios, discapacidad y salud.

El mapa permite seleccionar por nombre las alcaldías en población y las localidades del mismo nombre en origen y residencia. No se equipara la localidad con toda su demarcación. Milpa Alta tiene población en el archivo, pero no figura en las hojas de nacimiento, residencia o vivienda por alcaldía: se muestra **Sin dato**.

Cada tema ofrece gráficas y el tabulado completo con fuente por hoja. Las cantidades gráficas se redondean a enteros; los datos conservan precisión y la tabla muestra hasta seis decimales. No se convierten cantidades de ingresos en pesos ni se inventan universos que el Excel no documenta.

## Fuente y cálculos

`tabulados.js` contiene la extracción de las 13 hojas, con etiqueta original, fila de Excel, valores y notas. `tabulados-audit.json` contiene la huella SHA-256, filas por hoja y observaciones. Los nombres normalizados emparejan filas y mapa, retirando acentos, espacios y prefijos de localidad; se reconoce la errata «Gustvo A. Madero» como «Gustavo A. Madero», sin alterar su cifra ni la etiqueta del tabulado original.

Solo se calculan cocientes, diferencias y agregaciones dentro de los tabulados:

- Nacidos fuera de CDMX = otra entidad + Estados Unidos + otro país. Extranjero = Estados Unidos + otro país. Las notas del Excel incluyen país no especificado en otro país y entidad no especificada en no especificado.
- Residían fuera de CDMX en octubre de 2020 = otra entidad + Estados Unidos + otro país. Su universo es población de 5 años y más, distinto del de nacimiento.
- El resumen de origen/residencia se pondera con las poblaciones de las **15 localidades incluidas** y está rotulado como resumen calculado. No se extrapola a toda CDMX ni se imputa Milpa Alta. La población cubierta por nacimiento suma 8,775,278.
- Porcentajes por sexo = cantidades de mujeres/hombres de la hoja de población divididas entre su total. No se usan códigos de los microdatos.
- Cambios 2020–2025 = resta de cantidades y `(2025 / 2020 - 1) × 100`. La tabla expandida conserva las columnas originales de diferencias y estructura.
- Educación básica es un subtotal; sus tres niveles no se vuelven a sumar en la gráfica principal.
- Ingresos y salud se grafican por separado, sin sumar categorías ni asumir exclusividad.

## Observaciones conservadas

1. Vivienda por alcaldía: 15 filas suman 2,979,488 frente al total 3,022,557. La diferencia de 43,069 no se asigna a Milpa Alta.
2. Discapacidad CDMX: el encabezado solo dice **2020**. Los grupos suman 1,703,827 frente al total 1,703,791. No se presenta una cifra 2025 ni se corrige el total.
3. Ingresos CDMX: la columna Estructura utiliza el total nacional 39,699,242 como denominador. Se conserva en la tabla; las gráficas muestran cantidades.
4. Las notas de educación 1/–4/ fueron proporcionadas por el usuario como complemento al Excel y se muestran en ambos ámbitos: población de 3 años y más y las definiciones de estudios incluidos. Las notas de ingresos 1/–2/ proporcionadas por el usuario también se incorporaron en ambos ámbitos: porcentajes sobre el total de hogares, fuentes no excluyentes y definición de programas sociales. Las notas faltantes de salud no se infieren.
5. Los tabulados de origen/residencia incluyen la leyenda de precisión, pero no identifican en la extracción valores de CV o intervalos por fila; no se inventan niveles de confianza.

## Actualizar datos

```powershell
python -m pip install -r requirements.txt
python prepare_tabulados.py "C:\ruta\Data_Actualizada.xlsx"
```

El proceso genera `tabulados.js`, `tabulados-audit.json`, `dashboard.bundle.js` e incorpora su versión en `index.html`. Verifica filas esperadas, totales por sexo y sumas porcentuales. Conserva y muestra discrepancias de las hojas; no corrige las cifras automáticamente.

Para cambios de diseño o lógica, edita `tabulados-app.js`, `tabulados.css`, el HTML y los estilos compartidos; después ejecuta `python build_dashboard.py`. El bundle contiene únicamente `map.js`, `tabulados.js` y `tabulados-app.js`.

Los archivos heredados `app.js`, `explorer.js`, `data.js`, `reference.js`, `data-quality.json` y `prepare_data.py` pueden seguir en el repositorio para referencia histórica. **La página actual no los carga ni usa sus cifras.** El actualizador correcto es `prepare_tabulados.py`.

## Verificación

Se conciliaron 680 celdas de valores con el Excel extraído, se comprobaron las 13 hojas y 108 combinaciones de ámbito, tema y selección. Se verificaron las 16 regiones del mapa, la ausencia explícita de Milpa Alta donde corresponde y que el bundle no incluya datos de microdatos ni referencias poblacionales anteriores.

La vista de población de CDMX compara 2020 y 2025 para el total y cada alcaldía seleccionada, con cambio absoluto, porcentual, gráfica y tabla comparativa. La base 2020 se conserva en `population-city-2020.json`: tabla complementaria proporcionada por el usuario, relacionada por nombre con Poblacion Cdmx del Excel (2025). Sus 16 filas suman 9,209,944.
