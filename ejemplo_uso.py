"""
Ejemplo de uso del Sistema de Gestión de Biblioteca
Script de demostración sin interfaz interactiva
"""

from db import BaseDatos
from autores import GestorAutores
from libros import GestorLibros
from usuarios import GestorUsuarios
from prestamos import GestorPrestamos


def demo():
    """Función de demostración"""
    
    print("=" * 60)
    print("DEMO: Sistema de Gestión de Biblioteca")
    print("=" * 60)
    
    # Inicializar sistema
    print("\n[1] Inicializando base de datos...")
    db = BaseDatos("biblioteca_demo.db")
    
    # Crear gestores
    autores = GestorAutores(db)
    libros = GestorLibros(db)
    usuarios = GestorUsuarios(db)
    prestamos = GestorPrestamos(db)
    
    # ===== AGREGAR AUTORES =====
    print("\n[2] Agregando autores...")
    
    autor1_id = autores.agregar_autor(
        nombre="Gabriel García Márquez",
        fecha_nacimiento="1927-03-06",
        nacionalidad="Colombiano",
        biografia="Escritor y periodista colombiano, ganador del Premio Nobel de Literatura"
    )
    print(f"   ✓ Autor agregado: ID {autor1_id}")
    
    autor2_id = autores.agregar_autor(
        nombre="Jorge Luis Borges",
        fecha_nacimiento="1899-08-24",
        nacionalidad="Argentino",
        biografia="Escritor argentino, considerado uno de los autores más influyentes"
    )
    print(f"   ✓ Autor agregado: ID {autor2_id}")
    
    # ===== AGREGAR LIBROS =====
    print("\n[3] Agregando libros...")
    
    libro1_id = libros.agregar_libro(
        titulo="Cien años de soledad",
        id_autor=autor1_id,
        isbn="978-9584200051",
        año_publicacion=1967,
        editorial="Sudamericana",
        categoria="Realismo Mágico",
        cantidad_total=3,
        descripcion="Novela épica de García Márquez"
    )
    print(f"   ✓ Libro agregado: ID {libro1_id}")
    
    libro2_id = libros.agregar_libro(
        titulo="El Aleph",
        id_autor=autor2_id,
        isbn="978-9500305593",
        año_publicacion=1949,
        editorial="Emecé",
        categoria="Cuentos",
        cantidad_total=2,
        descripcion="Colección de cuentos de Borges"
    )
    print(f"   ✓ Libro agregado: ID {libro2_id}")
    
    # ===== AGREGAR USUARIOS =====
    print("\n[4] Agregando usuarios...")
    
    usuario1_id = usuarios.agregar_usuario(
        nombre="Juan Pérez García",
        email="juan.perez@universidad.edu",
        telefono="5551234567",
        direccion="Calle Principal 123",
        tipo_usuario="estudiante"
    )
    print(f"   ✓ Usuario agregado: ID {usuario1_id}")
    
    usuario2_id = usuarios.agregar_usuario(
        nombre="María López Rodríguez",
        email="maria.lopez@universidad.edu",
        telefono="5559876543",
        direccion="Avenida Secundaria 456",
        tipo_usuario="docente"
    )
    print(f"   ✓ Usuario agregado: ID {usuario2_id}")
    
    # ===== CREAR PRÉSTAMOS =====
    print("\n[5] Creando préstamos...")
    
    prestamo1_id = prestamos.crear_prestamo(
        id_usuario=usuario1_id,
        id_libro=libro1_id,
        dias_prestamo=14
    )
    print(f"   ✓ Préstamo creado: ID {prestamo1_id}")
    
    prestamo2_id = prestamos.crear_prestamo(
        id_usuario=usuario2_id,
        id_libro=libro2_id,
        dias_prestamo=21
    )
    print(f"   ✓ Préstamo creado: ID {prestamo2_id}")
    
    # ===== CONSULTAR INFORMACIÓN =====
    print("\n[6] Consultando información...")
    
    print("\n--- Todos los autores ---")
    todos_autores = autores.obtener_todos_autores()
    for autor in todos_autores:
        print(f"  {autor['id']}: {autor['nombre']} ({autor['nacionalidad']})")
    
    print("\n--- Todos los libros ---")
    todos_libros = libros.obtener_todos_libros()
    for libro in todos_libros:
        print(f"  {libro['id']}: {libro['titulo']} por {libro['autor_nombre']}")
        print(f"     Disponibles: {libro['cantidad_disponible']}/{libro['cantidad_total']}")
    
    print("\n--- Todos los usuarios ---")
    todos_usuarios = usuarios.obtener_todos_usuarios()
    for usuario in todos_usuarios:
        print(f"  {usuario['id']}: {usuario['nombre']} ({usuario['tipo_usuario']}) - {usuario['estado']}")
    
    print("\n--- Préstamos activos ---")
    prestamos_activos = prestamos.obtener_prestamos_activos()
    for prest in prestamos_activos:
        print(f"  {prest['id']}: {prest['usuario_nombre']} - {prest['libro_titulo']}")
        print(f"     Devolución esperada: {prest['fecha_devolucion_esperada']}")
    
    # ===== BÚSQUEDAS =====
    print("\n[7] Realizando búsquedas...")
    
    print("\n--- Búsqueda de autor 'García' ---")
    resultados = autores.buscar_autor("García")
    for autor in resultados:
        print(f"  {autor['nombre']}")
    
    print("\n--- Búsqueda de libro 'soledad' ---")
    resultados = libros.buscar_libro("soledad")
    for libro in resultados:
        print(f"  {libro['titulo']} - {libro['autor_nombre']}")
    
    # ===== ACTUALIZAR INFORMACIÓN =====
    print("\n[8] Actualizando información...")
    
    autores.actualizar_autor(
        autor1_id,
        biografia="Escritor colombiano, ganador del Premio Nobel de Literatura en 1982"
    )
    print(f"   ✓ Autor {autor1_id} actualizado")
    
    usuarios.cambiar_estado(usuario1_id, "inactivo")
    print(f"   ✓ Usuario {usuario1_id} marcado como inactivo")
    
    # ===== DEVOLVER LIBRO =====
    print("\n[9] Procesando devolución de libro...")
    
    resultado = prestamos.devolver_libro(prestamo1_id)
    if resultado:
        print(f"   ✓ Libro devuelto")
        print(f"     Días de retraso: {resultado['dias_retraso']}")
        print(f"     Multa: ${resultado['multa']:.2f}")
    
    # ===== ESTADÍSTICAS FINALES =====
    print("\n[10] Estadísticas finales...")
    
    print(f"   Total de autores: {len(todos_autores)}")
    print(f"   Total de libros: {len(todos_libros)}")
    print(f"   Total de usuarios: {len(todos_usuarios)}")
    print(f"   Préstamos activos: {len(prestamos_activos) - 1}")
    
    libros_disp = sum(1 for l in todos_libros if l['cantidad_disponible'] > 0)
    print(f"   Libros con disponibilidad: {libros_disp}")
    
    # Cerrar conexión
    db.cerrar()
    print("\n" + "=" * 60)
    print("✓ Demo completada exitosamente")
    print("=" * 60)


if __name__ == "__main__":
    try:
        demo()
    except Exception as e:
        print(f"\n✗ Error durante la demostración: {e}")
