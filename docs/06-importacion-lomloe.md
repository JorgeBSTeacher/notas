# Importación del Currículo LOMLOE

## Formato de importación

El archivo de importación puede ser **CSV** o **JSON**, con la siguiente estructura jerárquica:

### Formato JSON
```json
[
  {
    "codigo": "CC1",
    "descripcion": "Competencia en comunicación lingüística",
    "peso": 1.0,
    "competencias_especificas": [
      {
        "codigo": "CE1.1",
        "descripcion": "Comprender y producir textos orales",
        "peso": 1.0,
        "criterios": [
          {
            "codigo": "CRIT1.1.1",
            "descripcion": "Extraer información de textos orales",
            "peso": 1.0
          },
          {
            "codigo": "CRIT1.1.2",
            "descripcion": "Producir textos orales con coherencia",
            "peso": 1.0
          }
        ]
      }
    ]
  }
]
```

### Formato CSV
```csv
cc_codigo,cc_descripcion,cc_peso,ce_codigo,ce_descripcion,ce_peso,crit_codigo,crit_descripcion,crit_peso
CC1,Competencia comunicación lingüística,1.0,CE1.1,Comprender y producir textos orales,1.0,CRIT1.1.1,Extraer información de textos orales,1.0
CC1,Competencia comunicación lingüística,1.0,CE1.1,Comprender y producir textos orales,1.0,CRIT1.1.2,Producir textos orales con coherencia,1.0
```

## Fuentes oficiales

El currículo LOMLOE se publica en los reales decretos de enseñanzas mínimas y en los decretos autonómicos. Los códigos de los elementos curriculares varían por comunidad autónoma y materia.

### Estrategia de importación
1. **Archivo predefinido**: incluir un archivo JSON con el currículo por defecto de las materias más comunes (Matemáticas, Lengua, Inglés, etc.) para ESO y Bachillerato.
2. **Importación manual**: el profesor puede subir su propio archivo adaptado a su comunidad autónoma.
3. **Edición posterior**: tras la importación, el profesor puede modificar descripciones y pesos.

## Validaciones

- El sistema debe validar que no haya códigos duplicados dentro de una misma asignatura.
- Si se importa sobre un currículo existente, se debe preguntar si se desea:
  - **Sobrescribir**: reemplaza los elementos existentes (elimina los no presentes en el nuevo archivo).
  - **Actualizar**: añade nuevos elementos y actualiza descripciones, pero no elimina.
  - **Cancelar**.

## Esquema de códigos recomendado

- `CC{1-8}` para Competencias Clave (son fijas en LOMLOE: 8 competencias).
- `CE{materia}.{n}` para Competencias Específicas.
- `CRIT{materia}.{ce}.{n}` para Criterios de Evaluación.
