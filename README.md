# Personas · Explorador por alcaldía

Dashboard estático de los registros de `Personas_EncuestaIntercensal.xlsx`. Se abre con doble clic en `index.html` y funciona sin conexión, sin instalación y sin servicios externos. Mantén `index.html`, `styles.css`, `app.js` y `data.js` en la misma carpeta.

## Qué incluye

- Distribución por sexo en cada alcaldía, siguiendo la codificación proporcionada: 1 mujeres y 3 hombres.
- Nacionalidad mexicana, no mexicana y no especificada.
- Nacimiento en Ciudad de México, otra entidad de México, extranjero o no especificado.
- Ranking de entidades, países y otros lugares del catálogo por alcaldía, con conteos y porcentajes.
- Selector de alcaldía, vistas en porcentaje o conteo y tabla de cifras completas.

## Publicar en GitHub Pages

Sube el contenido de esta carpeta a la raíz de tu repositorio. Configura GitHub Pages para publicar desde la rama y carpeta que contengan `index.html` (habitualmente `main`, raíz). No requiere compilación. Las rutas relativas permiten usarlo en un repositorio de proyecto. Esta entrega no crea repositorios ni publica datos.

## Datos y alcance

Se cuenta una fila no vacía de `database` como un registro. El archivo no tiene factor de expansión; los resultados son conteos sin ponderar y no estimaciones de población. No se suma `NUMPER`, no se deduplican filas y no se infiere un identificador de persona u hogar. Los tamaños de muestra por alcaldía no deben interpretarse como tamaños relativos de su población.

La asignación de SEXO se basa en la instrucción del usuario, no en un diccionario oficial revisado. Confirma esta codificación antes de interpretar los resultados como distribución de mujeres y hombres.

`ENT_PAIS_NAC` se interpreta como lugar de nacimiento. No mide última residencia, procedencia inmediata ni migración reciente. No permite conocer el nacimiento en la misma alcaldía. Nacionalidad y lugar de nacimiento se presentan como conceptos distintos.

El catálogo `entidad` identifica los códigos 1–32 como entidades mexicanas. 9 corresponde a Ciudad de México. Códigos catalogados 100–536 se clasifican como extranjero (incluyen continentes, países y territorios). Los códigos 997, 998 y 999 se conservan como origen no especificado y se mantienen separados en el ranking, sin inferir que sean México o extranjero. Esto es una regla conservadora pendiente de confirmar con el diccionario de origen. No se reclasifican a partir de nacionalidad.

En la comparación, los porcentajes usan el total de cada alcaldía. En el ranking, incluso al filtrar México o extranjero, usan el total de las alcaldías seleccionadas. Los no especificados siguen formando parte del denominador. Por redondeo, los porcentajes pueden no sumar exactamente 100.0%.

La página está en español. No asigna año oficial a la encuesta a partir del nombre de la carpeta. Edad, escolaridad, pertenencia indígena, NUMPER y SM están fuera de esta primera versión.

## Actualizar desde otro Excel

Con Python instalado:

```powershell
python -m pip install -r requirements.txt
python prepare_data.py "C:\ruta\Personas_EncuestaIntercensal.xlsx"
```

El script lee las tres hojas, verifica claves duplicadas en catálogos y concilia los totales antes de generar `data.js` y `data-quality.json`. El Excel permanece intacto. Revisa el resumen y `data-quality.json` después de actualizar; contiene conteos de códigos originales, claves sin catálogo, filas vacías y la huella SHA-256 del archivo fuente. Recarga la página después de actualizar.

El navegador recibe conteos agregados por alcaldía y variable, sin filas individuales ni cruces de variables a nivel persona. El archivo original se mantiene fuera del sitio. La exclusión de Excel en `.gitignore` ayuda a mantenerlo separado del repositorio.

## Desarrollo

`index.html`: estructura; `styles.css`: diseño adaptable; `app.js`: filtros y gráficas; `data.js`: conteos. JavaScript y CSS nativos, sin dependencias de navegador. `prepare_data.py` requiere openpyxl únicamente para actualizar la extracción. La tabla desplegable presenta los valores exactos de cada barra y cada gráfica tiene una descripción accesible. Las categorías pequeñas se consultan en la tabla o al situar el cursor sobre la barra.
