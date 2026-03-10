# Runs

`runs/` guarda resultados de ejecuciones del proyecto.

## Idea general

Cada carpeta dentro de `runs/` representa una corrida. Ahí puedes guardar:

- tablas
- figuras
- logs
- una copia de la configuración usada

## Nombre sugerido

Usa algo fácil de leer, por ejemplo:

```text
2026-03-10__baseline
2026-03-10__sensibilidad
```

## Regla práctica

- Si el resultado se puede volver a generar, guárdalo en `runs/`.
- Si el resultado ya hace parte estable del proyecto, muévelo a `reports/` o `data/processed/`.
