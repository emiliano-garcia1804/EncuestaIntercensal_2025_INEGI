# Encuesta Intercensal · Ciudad de México

Dashboard estático de los registros de `Personas_EncuestaIntercensal.xlsx`. Se abre con doble clic en `index.html` y funciona sin conexión, sin instalación y sin servicios externos. Mantén todos los archivos HTML, CSS y JS de esta carpeta juntos.

## Estimación ajustada y mapa

La vista inicial aplica los porcentajes de la muestra a los totales por alcaldía de la columna 2025 de la imagen proporcionada por el usuario. Los 16 valores suman exactamente **9,165,819**. La tabla 2020 se conserva como referencia, pero ya no se usa para distribuir el total.

Para cada alcaldía: `factor = población 2025 / registros de la alcaldía`; `personas estimadas del grupo = registros del grupo × factor`. La cifra de CDMX suma las estimaciones de las 16 alcaldías. Los porcentajes dentro de cada alcaldía permanecen iguales; los porcentajes de CDMX se ponderan por los nuevos totales.

Los totales 2025 son datos proporcionados; la composición por origen es una estimación propia, no una expansión oficial de la encuesta. Se supone que los registros representan la composición dentro de cada alcaldía. No se dispone de probabilidades de selección ni diseño muestral para calcular márgenes de error. El universo de la primera imagen es viviendas particulares habitadas; no se ha confirmado su equivalencia exacta con el de la nueva tabla y el archivo. No se ajusta adicionalmente por sexo o edad. Las cantidades aproximadas se marcan con ≈ y los subtotales pueden diferir por redondeo.

Se transcribió Milpa Alta = 390,541 tal como aparece en la columna 2025; no se sustituyó ni corrigió a partir de su valor 2020. La fuente de los valores es la imagen del usuario, sin verificación externa de la publicación.

El selector de base permite volver a registros sin expandir. Nacidos fuera de CDMX agrupa otra entidad y extranjero. No mide migración reciente ni situación migratoria.

El mapa selecciona las alcaldías por clic o teclado y sincroniza las cifras y gráficas de origen. Usa polígonos del [Servicio Web de INEGI](https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgem/09), cuyo metadato indica Marco Geoestadístico, diciembre de 2025. Se incorpora la geometría localmente en `map.js` con proyección equirectangular ajustada a la latitud de CDMX; no usa mapas externos ni los campos poblacionales del servicio. Los colores representan porcentajes, con escala mínimo–máximo de las 16 alcaldías.

La distribución por edad y los porcentajes de sexo de la imagen se presentan como referencia para CDMX completa y no cambian al seleccionar una alcaldía. Sus cuatro grupos de edad suman 9,165,819. Los supuestos, insumos y factores por alcaldía también están en la sección desplegable del tablero.

## Qué incluye

- Distribución por sexo en cada alcaldía, siguiendo la codificación proporcionada: 1 mujeres y 3 hombres.
- Nacionalidad mexicana, no mexicana y no especificada.
- Nacimiento en Ciudad de México, otra entidad de México, extranjero o no especificado.
- Ranking de entidades, países y otros lugares del catálogo por alcaldía, con conteos y porcentajes.
- Selector de alcaldía, vistas en porcentaje o conteo y tabla de cifras completas.

## Publicar en GitHub Pages

Sube el contenido de esta carpeta a la raíz de tu repositorio. Configura GitHub Pages para publicar desde la rama y carpeta que contengan `index.html` (habitualmente `main`, raíz). No requiere compilación. Las rutas relativas permiten usarlo en un repositorio de proyecto. Esta entrega no crea repositorios ni publica datos.

## Datos y alcance

Se cuenta una fila no vacía de `database` como un registro. El archivo no tiene factor de expansión; el modo de registros presenta conteos sin ponderar y el modo de estimación usa el ajuste propio descrito arriba. No se suma `NUMPER`, no se deduplican filas y no se infiere un identificador de persona u hogar. Los tamaños de muestra por alcaldía no deben interpretarse como tamaños relativos de su población.

La asignación de SEXO se basa en la instrucción del usuario, no en un diccionario oficial revisado. Confirma esta codificación antes de interpretar los resultados como distribución de mujeres y hombres.

`ENT_PAIS_NAC` se interpreta como lugar de nacimiento. No mide última residencia, procedencia inmediata ni migración reciente. No permite conocer el nacimiento en la misma alcaldía. Nacionalidad y lugar de nacimiento se presentan como conceptos distintos.

El catálogo `entidad` identifica los códigos 1–32 como entidades mexicanas. 9 corresponde a Ciudad de México. Códigos catalogados 100–536 se clasifican como extranjero (incluyen continentes, países y territorios). Los códigos 997, 998 y 999 se conservan como origen no especificado y se mantienen separados en el ranking, sin inferir que sean México o extranjero. Esto es una regla conservadora pendiente de confirmar con el diccionario de origen. No se reclasifican a partir de nacionalidad.

En la comparación, los porcentajes usan el total de cada alcaldía. En el ranking, incluso al filtrar México o extranjero, usan el total de las alcaldías seleccionadas. Los no especificados siguen formando parte del denominador. Por redondeo, los porcentajes pueden no sumar exactamente 100.0%.

La página está en español. No asigna año oficial a la encuesta a partir del nombre de la carpeta. La edad de la imagen se muestra solo como referencia general. Edad de los registros individuales, escolaridad, pertenencia indígena, NUMPER y SM quedan fuera de este análisis.

## Actualizar desde otro Excel

Con Python instalado:

```powershell
python -m pip install -r requirements.txt
python prepare_data.py "C:\ruta\Personas_EncuestaIntercensal.xlsx"
```

El script lee las tres hojas, verifica claves duplicadas en catálogos y concilia los totales antes de generar `data.js` y `data-quality.json`. El Excel permanece intacto. Revisa el resumen y `data-quality.json` después de actualizar; contiene conteos de códigos originales, claves sin catálogo, filas vacías y la huella SHA-256 del archivo fuente. Recarga la página después de actualizar.

El navegador recibe conteos agregados por alcaldía y variable, sin filas individuales ni cruces de variables a nivel persona. El archivo original se mantiene fuera del sitio. La exclusión de Excel en `.gitignore` ayuda a mantenerlo separado del repositorio.

## Desarrollo

`index.html`: estructura; `styles.css` y `explorer.css`: diseño adaptable; `app.js`: filtros y gráficas; `explorer.js`: estimación, mapa y referencia; `data.js`: conteos; `map.js`: polígonos y procedencia; `reference.js`: total, poblaciones 2025, referencia 2020 y cifras de edad y sexo de la imagen. JavaScript y CSS nativos, sin dependencias de navegador. `prepare_data.py` requiere openpyxl únicamente para actualizar la extracción y conserva los insumos de referencia y mapa. Al cambiar los insumos poblacionales, actualiza `reference.js` y revisa que las claves coincidan con el catálogo.

Verificado: 612 combinaciones de base, alcaldía, variable, escala y filtro de origen; conciliación de la muestra y del total ajustado; correspondencia de las 16 claves con el mapa; selección de Cuauhtémoc mediante su polígono en el navegador. Se revisó visualmente el mapa. Las categorías pequeñas se consultan en la tabla o al situar el cursor sobre la barra.

## Carga y publicación

El navegador carga `dashboard.bundle.js`, que reúne datos, mapa, referencias y lógica en un solo archivo. El HTML incluye una versión por contenido para evitar mezclar archivos antiguos de la caché. Al modificar los archivos JS fuente, ejecuta `python build_dashboard.py` y publica también `index.html` y `dashboard.bundle.js`. Si falta el archivo principal se muestra un aviso, en lugar de dejar el mapa vacío.
