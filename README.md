# Sistema de Gestión de Ventas — Indumentaria y Calzado

Sistema de escritorio para la gestión de ventas, productos e inventario orientado a pequeños comercios de indumentaria y calzado. Desarrollado en Python con arquitectura en capas y persistencia en SQLite.

---

## Capturas de pantalla

> *Próximamente — el proyecto está en estado funcional.*

---

## Tecnologías utilizadas

- **Python 3.10+**
- **Tkinter** — interfaz gráfica de escritorio
- **SQLite 3** — base de datos local embebida
- **Pillow** — manejo de imágenes en la interfaz

---

## Arquitectura

El proyecto sigue una arquitectura de tres capas con separación estricta de responsabilidades:

```
modelo/         → Clases de dominio (Producto, Venta, DetalleVenta)
servicio/       → Lógica de negocio y validaciones
repositorio/    → Acceso a datos (SQL directo sobre SQLite)
vista/          → Interfaz gráfica con Tkinter
```

Ninguna capa accede directamente a la base de datos salvo `repositorio/`. La capa de vista nunca contiene lógica de negocio.

---

## Funcionalidades implementadas

- **Productos** — alta, consulta y baja lógica (el historial de ventas no se ve afectado)
- **Categorías** — alta, consulta y eliminación (con control de integridad referencial)
- **Ventas** — registro de ventas con múltiples productos por transacción
- **Cancelaciones** — cancelación de ventas con reintegro automático de stock
- **Reportes**
  - Ventas del día
  - Ventas por rango de fechas
  - Ranking de productos más vendidos
  - Valor total del inventario

---

## Estructura del proyecto

```
gestion-ventas-indumentaria/
├── docs/
│   ├── requerimientos.docx     ← Especificación de requerimientos (SRS)
│   └── diagrama_er.png         ← Diagrama entidad-relación
├── modelo/
│   ├── producto.py
│   └── venta.py
├── repositorio/
│   ├── database.py             ← Inicialización y conexión SQLite
│   ├── categoria_repo.py
│   ├── producto_repo.py
│   └── venta_repo.py
├── servicio/
│   ├── categoria_servicio.py
│   ├── producto_servicio.py
│   └── venta_servicio.py
├── vista/
│   ├── ventana_base.py
│   ├── ventana_principal.py
│   ├── ventana_categorias.py
│   ├── ventana_historial.py
│   └── ventana_reportes.py
├── main.py
├── requirements.txt
└── .gitignore
```

---

## Instalación y ejecución

### Requisitos previos

- Python 3.10 o superior
- pip

### Pasos

1. Cloná el repositorio:
   ```bash
   git clone https://github.com/benitezluciano/gestion-ventas-indumentaria.git
   cd gestion-ventas-indumentaria
   ```

2. Instalá las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutá la aplicación:
   ```bash
   python main.py
   ```

La base de datos (`ventas.db`) se crea automáticamente en el primer inicio.

### Primer uso

Al iniciar por primera vez el sistema no tiene datos cargados. El orden recomendado es:

1. Crear al menos una **categoría** desde el botón "Categorías"
2. Agregar **productos** asignándolos a esa categoría
3. Registrar **ventas** desde el botón "Realizar venta"

---

## Documentación

En la carpeta `docs/` se encuentran los artefactos de análisis producidos antes del desarrollo:

- **requerimientos.docx** — Especificación de Requerimientos de Software (SRS) con requerimientos funcionales (RF-01 a RF-25), requerimientos no funcionales, casos de uso y modelo de datos
- **diagrama_er.png** — Diagrama entidad-relación del modelo de base de datos

La documentación fue producida como etapa previa al desarrollo, siguiendo una metodología de diseño antes de codificación.

---

## Decisiones de diseño destacadas

**Baja lógica en productos** — Los productos no se eliminan físicamente de la base de datos. Se marcan como inactivos (`activo = 0`) para preservar la integridad del historial de ventas.

**Tabla `detalle_venta`** — Permite registrar múltiples productos por venta (relación N:M). Guarda el precio unitario al momento de la venta, garantizando que cambios futuros de precio no alteren el historial.

**Reintegro de stock al cancelar** — Al cancelar una venta, el sistema recupera los ítems de `detalle_venta` y reintegra automáticamente las unidades al stock de cada producto involucrado.

**Validaciones en capa de servicio** — Todas las reglas de negocio (stock suficiente, campos obligatorios, unicidad de SKU) se validan en `servicio/` antes de cualquier escritura en la base de datos.

---

## Mejoras planificadas

- **Buscador de productos en la ventana de venta** — actualmente el usuario debe ingresar el ID manualmente
- **Alertas visuales de stock mínimo** — el campo `stock_minimo` está implementado en el modelo pero aún no tiene representación visual
- **Selector de fechas en reportes** — reemplazar el ingreso manual de fechas por un DatePicker
- **Soporte para múltiples usuarios con roles** — la arquitectura está preparada para escalar, pendiente de implementación
- **Exportación de reportes a CSV o PDF**

---

## Contexto del proyecto

Este proyecto fue desarrollado como trabajo integrador de la carrera **Técnico Superior en Análisis Funcional de Sistemas Informáticos** en la Escuela Superior N°49, Rosario, Santa Fe.

El foco estuvo puesto en aplicar una metodología de análisis funcional completa: relevamiento de requerimientos, modelado de datos y definición de arquitectura antes de comenzar el desarrollo. El código resultante refleja esas decisiones de diseño previas.

---

## Autor

**Luciano Benitez**
Técnico Superior en Análisis Funcional de Sistemas Informáticos
[GitHub](https://github.com/benitezluciano)