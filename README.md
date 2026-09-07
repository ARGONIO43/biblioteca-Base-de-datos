# Sistema de Gestión de Biblioteca 

Sistema completo de gestión de biblioteca desarrollado en Python con base de datos SQLite, organizado en módulos para fácil mantenimiento y extensión.

## Características 

- **Gestión de Autores**: Crear, leer, actualizar y eliminar autores
- **Gestión de Libros**: Administrar catálogo de libros con inventario
- **Gestión de Usuarios**: Registrar estudiantes, docentes y personal administrativo
- **Gestión de Préstamos**: Crear préstamos, controlar devoluciones y calcular multas
- **Reportes**: Estadísticas, libros más prestados, usuarios activos, stock bajo
- **Base de Datos Relacional**: SQLite con relaciones entre tablas

## Estructura del Proyecto 

```
sistema-biblioteca/
├── __init__.py           # Paquete Python
├── db.py                 # Módulo de base de datos
├── autores.py           # CRUD de autores
├── libros.py            # CRUD de libros
├── usuarios.py          # CRUD de usuarios
├── prestamos.py         # CRUD de préstamos
├── main.py              # Interfaz principal
├── requirements.txt     # Dependencias
├── README.md            # Este archivo
└── .gitignore          # Archivos a ignorar en git
```

## Requisitos 

- Python 3.7 o superior
- No requiere instalación de paquetes externos (solo librerías estándar)

## Instalación 

1. **Clonar el repositorio:**
```bash
git clone 
cd sistema-biblioteca
```

2. **Verificar Python:**
```bash
python3 --version
```

3. **Ejecutar la aplicación:**
```bash
python3 main.py
```

## Uso 

### Menú Principal

Al ejecutar `main.py` se muestra un menú interactivo con las siguientes opciones:

```
1. Gestionar Autores
2. Gestionar Libros
3. Gestionar Usuarios
4. Gestionar Préstamos
5. Reportes
0. Salir
```

### Ejemplos de Uso

#### Agregar un Autor
1. Selecciona opción 1 (Gestionar Autores)
2. Selecciona 1 (Agregar autor)
3. Ingresa los datos solicitados

#### Agregar un Libro
1. Selecciona opción 2 (Gestionar Libros)
2. Selecciona 1 (Agregar libro)
3. Ingresa el ID del autor existente
4. Completa los datos del libro

#### Crear un Préstamo
1. Selecciona opción 4 (Gestionar Préstamos)
2. Selecciona 1 (Crear préstamo)
3. Ingresa el ID del usuario y del libro
4. Especifica los días de préstamo (default: 14 días)

#### Ver Reportes
1. Selecciona opción 5 (Reportes)
2. Elige el reporte deseado

## Modelos de Datos 

### Tabla: Autores
```sql
CREATE TABLE autores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    fecha_nacimiento DATE,
    nacionalidad TEXT,
    biografia TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Tabla: Libros
```sql
CREATE TABLE libros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    id_autor INTEGER NOT NULL,
    isbn TEXT UNIQUE NOT NULL,
    año_publicacion INTEGER,
    editorial TEXT,
    categoria TEXT,
    cantidad_total INTEGER DEFAULT 1,
    cantidad_disponible INTEGER DEFAULT 1,
    descripcion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_autor) REFERENCES autores(id)
)
```

### Tabla: Usuarios
```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    telefono TEXT,
    direccion TEXT,
    tipo_usuario TEXT DEFAULT 'estudiante',
    estado TEXT DEFAULT 'activo',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Tabla: Préstamos
```sql
CREATE TABLE prestamos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_libro INTEGER NOT NULL,
    fecha_prestamo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_devolucion_esperada DATE NOT NULL,
    fecha_devolucion_real DATE,
    estado TEXT DEFAULT 'activo',
    multa REAL DEFAULT 0.0,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_libro) REFERENCES libros(id)
)
```

## Funcionalidades por Módulo 🔌

### db.py - Gestión de Base de Datos
- `BaseDatos`: Clase principal para conexión SQLite
- `conectar()`: Establece conexión con la BD
- `crear_tablas()`: Crea las tablas relacional
- `ejecutar()`: Ejecuta queries de modificación
- `consultar()`: Ejecuta queries de lectura

### autores.py - Gestión de Autores
- `agregar_autor()`: Crear nuevo autor
- `obtener_autor()`: Obtener por ID
- `obtener_todos_autores()`: Listar todos
- `buscar_autor()`: Búsqueda por nombre
- `actualizar_autor()`: Modificar datos
- `eliminar_autor()`: Eliminar autor
- `obtener_libros_autor()`: Ver libros del autor

### libros.py - Gestión de Libros
- `agregar_libro()`: Crear nuevo libro
- `obtener_libro()`: Obtener por ID
- `obtener_todos_libros()`: Listar todos con autores
- `buscar_libro()`: Búsqueda por título, ISBN o categoría
- `obtener_por_categoria()`: Filtrar por categoría
- `actualizar_libro()`: Modificar datos
- `eliminar_libro()`: Eliminar libro
- `obtener_disponibles()`: Listar con stock
- `actualizar_disponibilidad()`: Controlar inventario

### usuarios.py - Gestión de Usuarios
- `agregar_usuario()`: Crear nuevo usuario
- `obtener_usuario()`: Obtener por ID
- `obtener_todos_usuarios()`: Listar todos
- `obtener_por_email()`: Búsqueda por email
- `buscar_usuario()`: Búsqueda por nombre
- `obtener_por_tipo()`: Filtrar por tipo
- `actualizar_usuario()`: Modificar datos
- `cambiar_estado()`: Activar/Inactivar
- `eliminar_usuario()`: Eliminar usuario
- `obtener_activos()`: Listar usuarios activos

### prestamos.py - Gestión de Préstamos
- `crear_prestamo()`: Registrar nuevo préstamo
- `obtener_prestamo()`: Obtener por ID
- `obtener_todos_prestamos()`: Listar todos
- `obtener_prestamos_activos()`: Préstamos sin devolver
- `obtener_prestamos_usuario()`: Préstamos de un usuario
- `obtener_prestamos_libro()`: Préstamos de un libro
- `devolver_libro()`: Registrar devolución y calcular multa
- `obtener_prestamos_retrasados()`: Préstamos vencidos
- `renovar_prestamo()`: Extender fecha de devolución

**Cálculo de Multas:**
- Multa diaria: $10.00
- Se calcula automáticamente al devolver libros retrasados

## Base de Datos 

El archivo `biblioteca.db` se crea automáticamente al ejecutar por primera vez.

**Para resetear la base de datos:**
```bash
rm biblioteca.db
python3 main.py
```

## Logging 

El sistema registra todas las operaciones en la consola con niveles:
- `INFO`: Operaciones exitosas
- `DEBUG`: Detalles de queries
- `WARNING`: Datos no encontrados
- `ERROR`: Problemas en operaciones

## Validaciones 

El sistema incluye validaciones para:
- Nombres únicos de autores y ISBNs
- Emails únicos de usuarios
- Cantidad disponible no negativa de libros
- Usuario activo para crear préstamos
- Libro con disponibilidad para préstamos
- Integridad referencial en la base de datos

## Desarrollo Futuro 

- [ ] Interfaz gráfica con tkinter o Qt
- [ ] Exportación a PDF de reportes
- [ ] Sistema de reservas de libros
- [ ] Integración con API REST
- [ ] Autenticación de usuarios
- [ ] Backup automático de la BD
- [ ] Histórico de cambios

## Contribuir 

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request



**Última actualización:** 2026 | **Versión:** 1.0.0
