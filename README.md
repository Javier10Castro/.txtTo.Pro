# .txtTo.Pro

Convertidor de archivos `.txt` a presentaciones nativas `.pro` para **ProPresenter 7**.

El proyecto automatiza la creación de presentaciones de canciones a partir de archivos de texto, utilizando una presentación `.pro` de referencia como plantilla.

## ¿Qué hace?

El convertidor:

1. Busca archivos `.txt` dentro de la carpeta `Canciones`.
2. Lee cada canción.
3. Utiliza las líneas en blanco para determinar la separación entre diapositivas.
4. Genera una presentación `.pro` independiente para cada canción.
5. Guarda las presentaciones generadas dentro de `SalidaPro`.

Por ejemplo:

```text
Primera línea
Segunda línea
Tercera línea

Cuarta línea
Quinta línea

Sexta línea
Séptima línea
```

se convierte en:

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

No es necesario utilizar `//` como separador.

---

## Requisitos

* Windows
* Python 3
* ProPresenter 7
* Una presentación `.pro` de referencia compatible con la versión de ProPresenter utilizada

El proyecto fue desarrollado y probado inicialmente con **ProPresenter 7.14.1**.

---

## Estructura

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

### `Canciones`

Aquí se colocan los archivos `.txt` que se quieren convertir.

### `SalidaPro`

Aquí se generan automáticamente los archivos `.pro`.

### `plantilla.pro`

Es la presentación `.pro` utilizada como referencia para construir las nuevas presentaciones.

### `convertir_txt_a_pro.py`

Contiene la lógica principal del convertidor.

### `convertir_pro.bat`

Permite ejecutar el convertidor fácilmente desde Windows sin tener que escribir el comando de Python manualmente.

---

## Formato de las canciones

Cada bloque separado por una línea en blanco representa una diapositiva.

Ejemplo:

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

Esto generará tres diapositivas.

### Importante

No es necesario escribir:

```text
//
```

La separación se realiza mediante líneas en blanco.

---

## Uso

### 1. Colocar las canciones

Copia los archivos `.txt` dentro de:

```text
Canciones/
```

### 2. Ejecutar el convertidor

Haz doble clic en:

```text
convertir_pro.bat
```

### 3. Revisar los resultados

Los archivos generados aparecerán en:

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

El archivo `.pro` puede abrirse posteriormente con ProPresenter.

---

## Clonar el proyecto en otra computadora

Para obtener el proyecto en otra computadora:

```bash
git clone https://github.com/Javier10Castro/.txtTo.Pro.git
```

Después:

```bash
cd .txtTo.Pro
```

Instala Python si la computadora no lo tiene y coloca la presentación `.pro` de referencia en la raíz del proyecto con el nombre:

```text
plantilla.pro
```

Después coloca las canciones `.txt` en:

```text
Canciones/
```

y ejecuta:

```text
convertir_pro.bat
```

---

## Compatibilidad

El formato `.pro` utilizado por ProPresenter es un formato binario y su estructura puede variar entre versiones de ProPresenter.

Por esta razón, `plantilla.pro` debe corresponder preferentemente a la versión de ProPresenter con la que se utilizarán las presentaciones generadas.

Versión de referencia actual:

```text
ProPresenter 7.14.1
```

Si se cambia de versión de ProPresenter, puede ser necesario generar una nueva `plantilla.pro` y adaptar el convertidor.

---

## Flujo de trabajo

```text
Canción .txt
     │
     ▼
convertir_pro.bat
     │
     ▼
convertir_txt_a_pro.py
     │
     ▼
plantilla.pro
     │
     ▼
Presentación .pro
     │
     ▼
SalidaPro/
```

---

## Estado del proyecto

Proyecto experimental / herramienta personal.

El objetivo principal es automatizar la preparación de canciones para ProPresenter y evitar tener que crear manualmente cada presentación y cada diapositiva.

---

## Autor

**Javier Ibrahim Castro**

GitHub:

https://github.com/Javier10Castro
