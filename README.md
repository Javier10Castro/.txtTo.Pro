# .txtTo.Pro

Convertidor de archivos `.txt` a presentaciones nativas `.pro` para **ProPresenter 7**.

El proyecto automatiza la creación de presentaciones de canciones a partir de archivos de texto, utilizando una presentación `.pro` de referencia como plantilla.

La idea es sencilla: **escribir las canciones en un archivo de texto, separar las diapositivas mediante líneas en blanco y dejar que el convertidor genere automáticamente las presentaciones `.pro`.**

---

## ¿Qué hace?

El convertidor:

1. Busca archivos `.txt` dentro de la carpeta `Canciones`.
2. Lee el contenido de cada canción.
3. Utiliza las líneas en blanco para determinar la separación entre diapositivas.
4. Utiliza `plantilla.pro` como presentación de referencia.
5. Genera una presentación `.pro` independiente para cada canción.
6. Guarda las presentaciones generadas dentro de `SalidaPro`.

Por ejemplo, un archivo:

```text
Primera línea
Segunda línea
Tercera línea

Cuarta línea
Quinta línea

Sexta línea
Séptima línea
```

se convierte en una presentación con:

```text
Slide 1
Primera línea
Segunda línea
Tercera línea

Slide 2
Cuarta línea
Quinta línea

Slide 3
Sexta línea
Séptima línea
```

No es necesario utilizar `//` como separador. **Una línea en blanco representa el cambio de diapositiva.**

---

## Requisitos

* Windows
* Python 3
* ProPresenter 7
* Una presentación `.pro` de referencia compatible con la versión de ProPresenter utilizada

El proyecto fue desarrollado y probado inicialmente con:

**ProPresenter 7.14.1**

> **Importante:** la presentación `plantilla.pro` es necesaria para generar correctamente los archivos `.pro`.

---

## Estructura del proyecto

```text
.txtTo.Pro/
│
├── Canciones/
│   └── .gitkeep
│
├── SalidaPro/
│   └── .gitkeep
│
├── convertir_txt_a_pro.py
├── convertir_pro.bat
├── plantilla.pro
├── .gitignore
└── README.md
```

### `Canciones/`

Carpeta donde se colocan los archivos `.txt` que se quieren convertir.

La carpeta ya está incluida en el repositorio para que esté disponible automáticamente después de clonar el proyecto.

### `SalidaPro/`

Carpeta donde se guardan automáticamente las presentaciones `.pro` generadas.

También está incluida en el repositorio.

### `plantilla.pro`

Presentación `.pro` utilizada como referencia para construir las nuevas presentaciones.

Se recomienda utilizar una plantilla creada con la misma versión de ProPresenter en la que posteriormente se utilizarán los archivos generados.

### `convertir_txt_a_pro.py`

Contiene la lógica principal del convertidor.

### `convertir_pro.bat`

Permite ejecutar el convertidor fácilmente en Windows mediante doble clic, sin necesidad de escribir manualmente el comando de Python.

---

## Formato de las canciones

Cada bloque de texto separado por una **línea en blanco** representa una diapositiva.

Por ejemplo:

```text
Abre mis ojos, oh Cristo
Abre mis ojos, Te pido
Yo quiero verte
Yo quiero verte

Y contemplar Tu majestad
Y el resplandor de Tu gloria
Derrama Tu amor y poder
Cuando cantamos: Santo, santo

Santo, santo, santo
Santo, santo, santo
```

El resultado será una presentación con tres diapositivas:

```text
Slide 1
Abre mis ojos, oh Cristo
Abre mis ojos, Te pido
Yo quiero verte
Yo quiero verte

Slide 2
Y contemplar Tu majestad
Y el resplandor de Tu gloria
Derrama Tu amor y poder
Cuando cantamos: Santo, santo

Slide 3
Santo, santo, santo
Santo, santo, santo
```

### Importante

No es necesario utilizar:

```text
//
```

La separación de diapositivas se realiza mediante **líneas en blanco**.

---

## Uso

### 1. Colocar las canciones

Copia los archivos `.txt` que deseas convertir dentro de:

```text
Canciones/
```

Por ejemplo:

```text
Canciones/
├── Abre mis ojos oh Cristo.txt
├── Santo por siempre.txt
└── Tu fidelidad.txt
```

### 2. Ejecutar el convertidor

Haz doble clic en:

```text
convertir_pro.bat
```

El script procesará los archivos `.txt` encontrados en `Canciones/`.

### 3. Revisar los resultados

Las presentaciones generadas aparecerán en:

```text
SalidaPro/
```

Por ejemplo:

```text
Canciones/
└── Abre mis ojos oh Cristo.txt

SalidaPro/
└── Abre mis ojos oh Cristo.pro
```

Cada archivo `.pro` generado corresponde a una de las canciones procesadas.

---

# Importar las canciones a ProPresenter

Una vez generados los archivos `.pro`, pueden importarse directamente a **ProPresenter 7**.

### 1. Abrir ProPresenter

Inicia ProPresenter 7.

### 2. Abrir el menú de importación

En la barra superior selecciona:

```text
File → Import → File
```

### 3. Seleccionar los archivos `.pro`

Busca la carpeta:

```text
SalidaPro/
```

Selecciona los archivos `.pro` que deseas importar.

Puedes seleccionar varias canciones al mismo tiempo utilizando las opciones de selección múltiple de Windows.

### 4. Confirmar la importación

Confirma la importación.

Las presentaciones aparecerán en ProPresenter y estarán disponibles para utilizarlas normalmente en tus servicios y presentaciones.

---

## Flujo completo

El flujo de trabajo recomendado es:

```text
                 ┌──────────────────┐
                 │   Canciones .txt  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ convertir_pro.bat│
                 └────────┬─────────┘
                          │
                          ▼
              ┌─────────────────────────┐
              │ convertir_txt_a_pro.py  │
              └────────────┬────────────┘
                           │
                           │ utiliza
                           ▼
                    ┌─────────────┐
                    │ plantilla.pro│
                    └──────┬──────┘
                           │
                           ▼
                 ┌──────────────────┐
                 │    SalidaPro/    │
                 │                  │
                 │   canciones.pro  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │    ProPresenter  │
                 │ File → Import    │
                 │      → File      │
                 └──────────────────┘
```

---

# Clonar el proyecto en otra computadora

Para obtener el proyecto en otra computadora, utiliza:

```bash
git clone https://github.com/Javier10Castro/.txtTo.Pro.git
```

Después entra a la carpeta:

```bash
cd .txtTo.Pro
```

Las carpetas necesarias del proyecto ya forman parte del repositorio:

```text
Canciones/
SalidaPro/
```

Si la computadora no tiene Python instalado, instala **Python 3** antes de ejecutar el convertidor.

La presentación de referencia debe encontrarse en la raíz del proyecto:

```text
plantilla.pro
```

Después:

1. Coloca los archivos `.txt` en `Canciones/`.
2. Verifica que `plantilla.pro` esté en la raíz del proyecto.
3. Ejecuta `convertir_pro.bat`.
4. Busca los archivos generados en `SalidaPro/`.
5. Importa los `.pro` en ProPresenter mediante:

```text
File → Import → File
```

---

## Compatibilidad

El formato `.pro` utilizado por ProPresenter es un formato binario y su estructura puede variar entre versiones de ProPresenter.

Por esta razón, `plantilla.pro` debe corresponder preferentemente a la versión de ProPresenter con la que se utilizarán las presentaciones generadas.

### Versión de referencia

```text
ProPresenter 7.14.1
```

Si se cambia de versión de ProPresenter, puede ser necesario generar una nueva `plantilla.pro` y adaptar el convertidor.

---

## Limitaciones

* El convertidor está diseñado para **ProPresenter 7**.
* Las líneas en blanco determinan la separación entre diapositivas.
* La presentación `plantilla.pro` es necesaria para generar los archivos.
* La compatibilidad con otras versiones de ProPresenter puede variar.
* El proyecto está orientado principalmente a Windows.

---

## Estado del proyecto

**Proyecto experimental / herramienta personal.**

El objetivo principal es automatizar la preparación de canciones para ProPresenter y evitar tener que crear manualmente cada presentación y cada diapositiva.

---

## Autor

**Javier Ibrahim Castro**

GitHub:

https://github.com/Javier10Castro
