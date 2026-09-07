# Guía Rápida - Sistema de Gestión de Biblioteca 🚀

## Instalación Rápida (5 minutos)


###  Verificar Python

```bash
python3 --version
# Debe ser 3.7 o superior
```

### 3️⃣ Ejecutar

```bash
python3 main.py
```

¡Eso es todo! 

---

## Primeros Pasos

### Agregar tu Primer Autor
1. Selecciona opción **1** (Gestionar Autores)
2. Selecciona **1** (Agregar autor)
3. Ingresa: Nombre, Fecha de nacimiento (opcional), Nacionalidad, Biografía
4. ¡Listo! Tu autor está registrado

### Agregar tu Primer Libro
1. Selecciona opción **2** (Gestionar Libros)
2. Selecciona **1** (Agregar libro)
3. Ingresa el **ID del autor** (verás los disponibles)
4. Completa: Título, ISBN, Año, Editorial, Categoría, Cantidad
5. ¡Listo! Tu libro está en el catálogo

### Registrar un Usuario
1. Selecciona opción **3** (Gestionar Usuarios)
2. Selecciona **1** (Agregar usuario)
3. Ingresa: Nombre, Email, Teléfono, Dirección, Tipo
4. ¡Listo! El usuario está registrado

### Crear un Préstamo
1. Selecciona opción **4** (Gestionar Préstamos)
2. Selecciona **1** (Crear préstamo)
3. Ingresa: **ID Usuario**, **ID Libro**, Días de préstamo (default 14)
4. ¡Listo! El préstamo está registrado

---

## Comandos Útiles

### Listar Información
- **Ver todos los libros**: Opción 2 → 2
- **Ver todos los usuarios**: Opción 3 → 2
- **Ver préstamos activos**: Opción 4 → 3

### Buscar
- **Buscar libro**: Opción 2 → 3
- **Buscar usuario**: Opción 3 → 3
- **Buscar autor**: Opción 1 → 3

### Ver Reportes
- **Estadísticas**: Opción 5 → 1
- **Libros más prestados**: Opción 5 → 2
- **Usuarios activos**: Opción 5 → 3

---

## Devolución de Libros y Multas

### Devolver un Libro
1. Opción 4 (Gestionar Préstamos)
2. Selecciona 5 (Devolver libro)
3. Ingresa el **ID del préstamo**
4. ¡Automático! Se calcula la multa si hay retraso

### Cálculo de Multas
- **Multa diaria**: $10.00
- **Se calcula solo si**: La devolución es después de la fecha esperada

### Ejemplo
- Préstamo esperado para: 15 de septiembre
- Devolución real: 20 de septiembre
- Retraso: 5 días
- Multa: 5 × $10 = $50.00

---

## Estructura de la Base de Datos

```
Tabla: AUTORES
├── id (único)
├── nombre (único)
├── fecha_nacimiento
├── nacionalidad
├── biografia
└── fecha_registro

Tabla: LIBROS
├── id (único)
├── título
├── id_autor (vinculado a AUTORES)
├── isbn (único)
├── año_publicación
├── editorial
├── categoría
├── cantidad_total
├── cantidad_disponible
├── descripción
└── fecha_registro

Tabla: USUARIOS
├── id (único)
├── nombre
├── email (único)
├── teléfono
├── dirección
├── tipo_usuario (estudiante, docente, administrativo)
├── estado (activo, inactivo)
└── fecha_registro

Tabla: PRÉSTAMOS
├── id (único)
├── id_usuario (vinculado a USUARIOS)
├── id_libro (vinculado a LIBROS)
├── fecha_préstamo
├── fecha_devolución_esperada
├── fecha_devolución_real
├── estado (activo, devuelto)
└── multa
```

---

## Subir a GitHub 📤

```bash
# Inicializar repositorio
git init

# Agregar archivos
git add .

# Hacer commit
git commit -m "Proyecto inicial: Sistema de Gestión de Biblioteca"

# Agregar repositorio remoto
git remote add origin https://github.com/TuUsuario/sistema-biblioteca.git

# Push al repositorio
git branch -M main
git push -u origin main
```

---

## Solucionar Problemas 🔧

### Error: "No se puede importar db"
**Solución**: Asegúrate de estar en la carpeta correcta
```bash
cd sistema-biblioteca
python3 main.py
```

### Error: "ID inválido"
**Solución**: Ingresa solo números, usa IDs que existan
```bash
# Primero lista los items para ver sus IDs
Opción → Ver todos → Anotate los IDs
```

### Base de datos corrupta
**Solución**: Elimina el archivo y crea uno nuevo
```bash
rm biblioteca.db
python3 main.py
```

---

## Probar con Demo

```bash
python3 ejemplo_uso.py
```

Este script muestra un ejemplo completo sin interfaz interactiva.

---

## Archivos Importantes

| Archivo | Descripción |
|---------|-------------|
| `main.py` | Interfaz principal interactiva |
| `db.py` | Gestión de base de datos |
| `autores.py` | Módulo de autores |
| `libros.py` | Módulo de libros |
| `usuarios.py` | Módulo de usuarios |
| `prestamos.py` | Módulo de préstamos |
| `biblioteca.db` | Base de datos SQLite (se crea automáticamente) |

---

## Tips Importantes 

1. **Antes de agregar un libro**, debes agregar un autor
2. **Antes de crear un préstamo**, debes agregar usuario y libro
3. **Los emails deben ser únicos** por usuario
4. **Los ISBNs deben ser únicos** por libro
5. **Los nombres deben ser únicos** por autor
6. **Solo usuarios activos** pueden hacer préstamos
7. **Solo libros con disponibilidad** pueden ser prestados

---

## Próximas Mejoras Planeadas 

- [ ] Interfaz gráfica
- [ ] Exportación a PDF
- [ ] Sistema de reservas
- [ ] API REST
- [ ] Autenticación
- [ ] Backup automático


