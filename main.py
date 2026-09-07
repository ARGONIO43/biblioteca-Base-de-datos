"""
Sistema de Gestión de Biblioteca
Interfaz principal con menú interactivo
"""

import os
from datetime import datetime
from db import BaseDatos
from autores import GestorAutores
from libros import GestorLibros
from usuarios import GestorUsuarios
from prestamos import GestorPrestamos


class SistemaBiblioteca:
    """Sistema principal de gestión de biblioteca"""
    
    def __init__(self, nombre_db="biblioteca.db"):
        """Inicializa el sistema"""
        self.db = BaseDatos(nombre_db)
        self.autores = GestorAutores(self.db)
        self.libros = GestorLibros(self.db)
        self.usuarios = GestorUsuarios(self.db)
        self.prestamos = GestorPrestamos(self.db)
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal"""
        self.limpiar_pantalla()
        print("=" * 50)
        print("   SISTEMA DE GESTIÓN DE BIBLIOTECA")
        print("=" * 50)
        print("\n1. Gestionar Autores")
        print("2. Gestionar Libros")
        print("3. Gestionar Usuarios")
        print("4. Gestionar Préstamos")
        print("5. Reportes")
        print("0. Salir")
        print("\n" + "=" * 50)
    
    def menu_autores(self):
        """Menú de gestión de autores"""
        while True:
            self.limpiar_pantalla()
            print("=== GESTIÓN DE AUTORES ===\n")
            print("1. Agregar autor")
            print("2. Ver todos los autores")
            print("3. Buscar autor")
            print("4. Ver libros de un autor")
            print("5. Actualizar autor")
            print("6. Eliminar autor")
            print("0. Volver")
            
            opcion = input("\nSeleccione opción: ").strip()
            
            if opcion == "1":
                self._agregar_autor()
            elif opcion == "2":
                self._ver_autores()
            elif opcion == "3":
                self._buscar_autor()
            elif opcion == "4":
                self._ver_libros_autor()
            elif opcion == "5":
                self._actualizar_autor()
            elif opcion == "6":
                self._eliminar_autor()
            elif opcion == "0":
                break
            else:
                input("Opción inválida. Presione Enter para continuar...")
    
    def _agregar_autor(self):
        """Agrega un nuevo autor"""
        self.limpiar_pantalla()
        print("=== AGREGAR AUTOR ===\n")
        
        nombre = input("Nombre del autor: ").strip()
        if not nombre:
            print("El nombre no puede estar vacío")
            input("Presione Enter para continuar...")
            return
        
        fecha_nac = input("Fecha de nacimiento (YYYY-MM-DD) [opcional]: ").strip() or None
        nacionalidad = input("Nacionalidad [opcional]: ").strip() or None
        biografia = input("Biografía [opcional]: ").strip() or None
        
        try:
            id_autor = self.autores.agregar_autor(nombre, fecha_nac, nacionalidad, biografia)
            print(f"\n✓ Autor agregado exitosamente con ID {id_autor}")
        except Exception as e:
            print(f"\n✗ Error: {e}")
        
        input("Presione Enter para continuar...")
    
    def _ver_autores(self):
        """Muestra todos los autores"""
        self.limpiar_pantalla()
        print("=== LISTA DE AUTORES ===\n")
        
        try:
            autores = self.autores.obtener_todos_autores()
            if not autores:
                print("No hay autores registrados")
            else:
                print(f"{'ID':<5} {'Nombre':<30} {'Nacionalidad':<20}")
                print("-" * 55)
                for autor in autores:
                    print(f"{autor['id']:<5} {autor['nombre']:<30} {autor['nacionalidad'] or 'N/A':<20}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _buscar_autor(self):
        """Busca un autor por nombre"""
        self.limpiar_pantalla()
        print("=== BUSCAR AUTOR ===\n")
        
        nombre = input("Ingrese el nombre a buscar: ").strip()
        if not nombre:
            print("Debe ingresar un nombre")
            input("Presione Enter para continuar...")
            return
        
        try:
            autores = self.autores.buscar_autor(nombre)
            if not autores:
                print("No se encontraron autores")
            else:
                print(f"\nResultados encontrados: {len(autores)}\n")
                print(f"{'ID':<5} {'Nombre':<30}")
                print("-" * 35)
                for autor in autores:
                    print(f"{autor['id']:<5} {autor['nombre']:<30}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _ver_libros_autor(self):
        """Ve los libros de un autor"""
        self.limpiar_pantalla()
        print("=== LIBROS DE UN AUTOR ===\n")
        
        id_autor = input("Ingrese el ID del autor: ").strip()
        if not id_autor.isdigit():
            print("ID inválido")
            input("Presione Enter para continuar...")
            return
        
        try:
            libros = self.autores.obtener_libros_autor(int(id_autor))
            if not libros:
                print("No hay libros registrados para este autor")
            else:
                print(f"\n{'ID':<5} {'Título':<30} {'ISBN':<15} {'Disponibles':<12}")
                print("-" * 62)
                for libro in libros:
                    print(f"{libro['id']:<5} {libro['titulo']:<30} {libro['isbn']:<15} {libro['cantidad_disponible']:<12}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _actualizar_autor(self):
        """Actualiza información de un autor"""
        self.limpiar_pantalla()
        print("=== ACTUALIZAR AUTOR ===\n")
        
        id_autor = input("Ingrese el ID del autor: ").strip()
        if not id_autor.isdigit():
            print("ID inválido")
            input("Presione Enter para continuar...")
            return
        
        print("\n¿Qué desea actualizar? (dejar en blanco para no cambiar)")
        nombre = input("Nuevo nombre: ").strip() or None
        nacionalidad = input("Nueva nacionalidad: ").strip() or None
        biografia = input("Nueva biografía: ").strip() or None
        
        try:
            kwargs = {}
            if nombre:
                kwargs['nombre'] = nombre
            if nacionalidad:
                kwargs['nacionalidad'] = nacionalidad
            if biografia:
                kwargs['biografia'] = biografia
            
            if kwargs:
                if self.autores.actualizar_autor(int(id_autor), **kwargs):
                    print("\n✓ Autor actualizado exitosamente")
                else:
                    print("\n✗ No se pudo actualizar el autor")
            else:
                print("\nNo hay cambios para realizar")
        except Exception as e:
            print(f"\n✗ Error: {e}")
        
        input("Presione Enter para continuar...")
    
    def _eliminar_autor(self):
        """Elimina un autor"""
        self.limpiar_pantalla()
        print("=== ELIMINAR AUTOR ===\n")
        
        id_autor = input("Ingrese el ID del autor a eliminar: ").strip()
        if not id_autor.isdigit():
            print("ID inválido")
            input("Presione Enter para continuar...")
            return
        
        confirmacion = input("¿Está seguro? Esto también eliminará sus libros (s/n): ").strip().lower()
        if confirmacion == 's':
            try:
                if self.autores.eliminar_autor(int(id_autor)):
                    print("\n✓ Autor eliminado exitosamente")
                else:
                    print("\n✗ Autor no encontrado")
            except Exception as e:
                print(f"\n✗ Error: {e}")
        
        input("Presione Enter para continuar...")
    
    def menu_libros(self):
        """Menú de gestión de libros"""
        while True:
            self.limpiar_pantalla()
            print("=== GESTIÓN DE LIBROS ===\n")
            print("1. Agregar libro")
            print("2. Ver todos los libros")
            print("3. Buscar libro")
            print("4. Ver libros disponibles")
            print("5. Actualizar libro")
            print("6. Eliminar libro")
            print("0. Volver")
            
            opcion = input("\nSeleccione opción: ").strip()
            
            if opcion == "1":
                self._agregar_libro()
            elif opcion == "2":
                self._ver_libros()
            elif opcion == "3":
                self._buscar_libro()
            elif opcion == "4":
                self._ver_libros_disponibles()
            elif opcion == "5":
                self._actualizar_libro()
            elif opcion == "6":
                self._eliminar_libro()
            elif opcion == "0":
                break
            else:
                input("Opción inválida. Presione Enter para continuar...")
    
    def _agregar_libro(self):
        """Agrega un nuevo libro"""
        self.limpiar_pantalla()
        print("=== AGREGAR LIBRO ===\n")
        
        titulo = input("Título del libro: ").strip()
        if not titulo:
            print("El título no puede estar vacío")
            input("Presione Enter para continuar...")
            return
        
        # Mostrar autores disponibles
        autores = self.autores.obtener_todos_autores()
        if not autores:
            print("Debe crear al menos un autor primero")
            input("Presione Enter para continuar...")
            return
        
        print("\nAutores disponibles:")
        for autor in autores:
            print(f"  {autor['id']}: {autor['nombre']}")
        
        id_autor = input("\nSeleccione ID del autor: ").strip()
        if not id_autor.isdigit():
            print("ID inválido")
            input("Presione Enter para continuar...")
            return
        
        isbn = input("ISBN (único): ").strip()
        if not isbn:
            print("El ISBN no puede estar vacío")
            input("Presione Enter para continuar...")
            return
        
        año = input("Año de publicación [opcional]: ").strip() or None
        if año:
            try:
                año = int(año)
            except ValueError:
                año = None
        
        editorial = input("Editorial [opcional]: ").strip() or None
        categoria = input("Categoría [opcional]: ").strip() or None
        cantidad = input("Cantidad de ejemplares [1]: ").strip() or "1"
        
        try:
            cantidad = int(cantidad)
            id_libro = self.libros.agregar_libro(
                titulo, int(id_autor), isbn, año, editorial, categoria, cantidad
            )
            print(f"\n✓ Libro agregado exitosamente con ID {id_libro}")
        except ValueError:
            print("\n✗ Cantidad inválida")
        except Exception as e:
            print(f"\n✗ Error: {e}")
        
        input("Presione Enter para continuar...")
    
    def _ver_libros(self):
        """Muestra todos los libros"""
        self.limpiar_pantalla()
        print("=== LISTA DE LIBROS ===\n")
        
        try:
            libros = self.libros.obtener_todos_libros()
            if not libros:
                print("No hay libros registrados")
            else:
                print(f"{'ID':<5} {'Título':<25} {'Autor':<20} {'Disponibles':<12}")
                print("-" * 62)
                for libro in libros:
                    print(f"{libro['id']:<5} {libro['titulo']:<25} {libro['autor_nombre']:<20} {libro['cantidad_disponible']:<12}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _buscar_libro(self):
        """Busca un libro"""
        self.limpiar_pantalla()
        print("=== BUSCAR LIBRO ===\n")
        
        termino = input("Ingrese término de búsqueda (título, ISBN o categoría): ").strip()
        if not termino:
            print("Debe ingresar un término")
            input("Presione Enter para continuar...")
            return
        
        try:
            libros = self.libros.buscar_libro(termino)
            if not libros:
                print("No se encontraron libros")
            else:
                print(f"\nResultados encontrados: {len(libros)}\n")
                print(f"{'ID':<5} {'Título':<25} {'Autor':<20} {'Disponibles':<12}")
                print("-" * 62)
                for libro in libros:
                    print(f"{libro['id']:<5} {libro['titulo']:<25} {libro['autor_nombre']:<20} {libro['cantidad_disponible']:<12}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _ver_libros_disponibles(self):
        """Muestra solo libros disponibles"""
        self.limpiar_pantalla()
        print("=== LIBROS DISPONIBLES ===\n")
        
        try:
            libros = self.libros.obtener_disponibles()
            if not libros:
                print("No hay libros disponibles")
            else:
                print(f"{'ID':<5} {'Título':<25} {'Autor':<20} {'Disponibles':<12}")
                print("-" * 62)
                for libro in libros:
                    print(f"{libro['id']:<5} {libro['titulo']:<25} {libro['autor_nombre']:<20} {libro['cantidad_disponible']:<12}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _actualizar_libro(self):
        """Actualiza información de un libro"""
        self.limpiar_pantalla()
        print("=== ACTUALIZAR LIBRO ===\n")
        
        id_libro = input("Ingrese el ID del libro: ").strip()
        if not id_libro.isdigit():
            print("ID inválido")
            input("Presione Enter para continuar...")
            return
        
        print("\n¿Qué desea actualizar? (dejar en blanco para no cambiar)")
        titulo = input("Nuevo título: ").strip() or None
        editorial = input("Nueva editorial: ").strip() or None
        
        try:
            kwargs = {}
            if titulo:
                kwargs['titulo'] = titulo
            if editorial:
                kwargs['editorial'] = editorial
            
            if kwargs:
                if self.libros.actualizar_libro(int(id_libro), **kwargs):
                    print("\n✓ Libro actualizado exitosamente")
                else:
                    print("\n✗ No se pudo actualizar el libro")
            else:
                print("\nNo hay cambios para realizar")
        except Exception as e:
            print(f"\n✗ Error: {e}")
        
        input("Presione Enter para continuar...")
    
    def _eliminar_libro(self):
        """Elimina un libro"""
        self.limpiar_pantalla()
        print("=== ELIMINAR LIBRO ===\n")
        
        id_libro = input("Ingrese el ID del libro a eliminar: ").strip()
        if not id_libro.isdigit():
            print("ID inválido")
            input("Presione Enter para continuar...")
            return
        
        confirmacion = input("¿Está seguro? (s/n): ").strip().lower()
        if confirmacion == 's':
            try:
                if self.libros.eliminar_libro(int(id_libro)):
                    print("\n✓ Libro eliminado exitosamente")
                else:
                    print("\n✗ Libro no encontrado")
            except Exception as e:
                print(f"\n✗ Error: {e}")
        
        input("Presione Enter para continuar...")
    
    def menu_usuarios(self):
        """Menú de gestión de usuarios"""
        while True:
            self.limpiar_pantalla()
            print("=== GESTIÓN DE USUARIOS ===\n")
            print("1. Agregar usuario")
            print("2. Ver todos los usuarios")
            print("3. Buscar usuario")
            print("4. Ver usuarios activos")
            print("5. Actualizar usuario")
            print("6. Cambiar estado")
            print("7. Eliminar usuario")
            print("0. Volver")
            
            opcion = input("\nSeleccione opción: ").strip()
            
            if opcion == "1":
                self._agregar_usuario()
            elif opcion == "2":
                self._ver_usuarios()
            elif opcion == "3":
                self._buscar_usuario()
            elif opcion == "4":
                self._ver_usuarios_activos()
            elif opcion == "5":
                self._actualizar_usuario()
            elif opcion == "6":
                self._cambiar_estado_usuario()
            elif opcion == "7":
                self._eliminar_usuario()
            elif opcion == "0":
                break
            else:
                input("Opción inválida. Presione Enter para continuar...")
    
    def _agregar_usuario(self):
        """Agrega un nuevo usuario"""
        self.limpiar_pantalla()
        print("=== AGREGAR USUARIO ===\n")
        
        nombre = input("Nombre del usuario: ").strip()
        if not nombre:
            print("El nombre no puede estar vacío")
            input("Presione Enter para continuar...")
            return
        
        email = input("Email (único): ").strip()
        if not email:
            print("El email no puede estar vacío")
            input("Presione Enter para continuar...")
            return
        
        telefono = input("Teléfono [opcional]: ").strip() or None
        direccion = input("Dirección [opcional]: ").strip() or None
        
        print("\nTipo de usuario: (1) Estudiante, (2) Docente, (3) Administrativo")
        tipo_opcion = input("Seleccione [1]: ").strip() or "1"
        tipos = {"1": "estudiante", "2": "docente", "3": "administrativo"}
        tipo_usuario = tipos.get(tipo_opcion, "estudiante")
        
        try:
            id_usuario = self.usuarios.agregar_usuario(nombre, email, telefono, direccion, tipo_usuario)
            print(f"\n✓ Usuario agregado exitosamente con ID {id_usuario}")
        except Exception as e:
            print(f"\n✗ Error: {e}")
        
        input("Presione Enter para continuar...")
    
    def _ver_usuarios(self):
        """Muestra todos los usuarios"""
        self.limpiar_pantalla()
        print("=== LISTA DE USUARIOS ===\n")
        
        try:
            usuarios = self.usuarios.obtener_todos_usuarios()
            if not usuarios:
                print("No hay usuarios registrados")
            else:
                print(f"{'ID':<5} {'Nombre':<25} {'Email':<25} {'Tipo':<15} {'Estado':<10}")
                print("-" * 80)
                for usuario in usuarios:
                    print(f"{usuario['id']:<5} {usuario['nombre']:<25} {usuario['email']:<25} {usuario['tipo_usuario']:<15} {usuario['estado']:<10}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _buscar_usuario(self):
        """Busca un usuario por nombre"""
        self.limpiar_pantalla()
        print("=== BUSCAR USUARIO ===\n")
        
        nombre = input("Ingrese el nombre a buscar: ").strip()
        if not nombre:
            print("Debe ingresar un nombre")
            input("Presione Enter para continuar...")
            return
        
        try:
            usuarios = self.usuarios.buscar_usuario(nombre)
            if not usuarios:
                print("No se encontraron usuarios")
            else:
                print(f"\nResultados encontrados: {len(usuarios)}\n")
                print(f"{'ID':<5} {'Nombre':<25} {'Email':<25} {'Tipo':<15}")
                print("-" * 70)
                for usuario in usuarios:
                    print(f"{usuario['id']:<5} {usuario['nombre']:<25} {usuario['email']:<25} {usuario['tipo_usuario']:<15}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _ver_usuarios_activos(self):
        """Muestra solo usuarios activos"""
        self.limpiar_pantalla()
        print("=== USUARIOS ACTIVOS ===\n")
        
        try:
            usuarios = self.usuarios.obtener_activos()
            if not usuarios:
                print("No hay usuarios activos")
            else:
                print(f"{'ID':<5} {'Nombre':<25} {'Email':<25} {'Tipo':<15}")
                print("-" * 70)
                for usuario in usuarios:
                    print(f"{usuario['id']:<5} {usuario['nombre']:<25} {usuario['email']:<25} {usuario['tipo_usuario']:<15}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _actualizar_usuario(self):
        """Actualiza información de un usuario"""
        self.limpiar_pantalla()
        print("=== ACTUALIZAR USUARIO ===\n")
        
        id_usuario = input("Ingrese el ID del usuario: ").strip()
        if not id_usuario.isdigit():
            print("ID inválido")
            input("Presione Enter para continuar...")
            return
        
        print("\n¿Qué desea actualizar? (dejar en blanco para no cambiar)")
        nombre = input("Nuevo nombre: ").strip() or None
        telefono = input("Nuevo teléfono: ").strip() or None
        direccion = input("Nueva dirección: ").strip() or None
        
        try:
            kwargs = {}
            if nombre:
                kwargs['nombre'] = nombre
            if telefono:
                kwargs['telefono'] = telefono
            if direccion:
                kwargs['direccion'] = direccion
            
            if kwargs:
                if self.usuarios.actualizar_usuario(int(id_usuario), **kwargs):
                    print("\n✓ Usuario actualizado exitosamente")
                else:
                    print("\n✗ No se pudo actualizar el usuario")
            else:
                print("\nNo hay cambios para realizar")
        except Exception as e:
            print(f"\n✗ Error: {e}")
        
        input("Presione Enter para continuar...")
    
    def _cambiar_estado_usuario(self):
        """Cambia el estado de un usuario"""
        self.limpiar_pantalla()
        print("=== CAMBIAR ESTADO DE USUARIO ===\n")
        
        id_usuario = input("Ingrese el ID del usuario: ").strip()
        if not id_usuario.isdigit():
            print("ID inválido")
            input("Presione Enter para continuar...")
            return
        
        print("\nEstados: (1) Activo, (2) Inactivo")
        opcion = input("Seleccione nuevo estado: ").strip()
        estados = {"1": "activo", "2": "inactivo"}
        
        if opcion not in estados:
            print("Opción inválida")
            input("Presione Enter para continuar...")
            return
        
        try:
            if self.usuarios.cambiar_estado(int(id_usuario), estados[opcion]):
                print(f"\n✓ Estado cambiado a {estados[opcion]}")
            else:
                print("\n✗ No se pudo cambiar el estado")
        except Exception as e:
            print(f"\n✗ Error: {e}")
        
        input("Presione Enter para continuar...")
    
    def _eliminar_usuario(self):
        """Elimina un usuario"""
        self.limpiar_pantalla()
        print("=== ELIMINAR USUARIO ===\n")
        
        id_usuario = input("Ingrese el ID del usuario a eliminar: ").strip()
        if not id_usuario.isdigit():
            print("ID inválido")
            input("Presione Enter para continuar...")
            return
        
        confirmacion = input("¿Está seguro? (s/n): ").strip().lower()
        if confirmacion == 's':
            try:
                if self.usuarios.eliminar_usuario(int(id_usuario)):
                    print("\n✓ Usuario eliminado exitosamente")
                else:
                    print("\n✗ Usuario no encontrado")
            except Exception as e:
                print(f"\n✗ Error: {e}")
        
        input("Presione Enter para continuar...")
    
    def menu_prestamos(self):
        """Menú de gestión de préstamos"""
        while True:
            self.limpiar_pantalla()
            print("=== GESTIÓN DE PRÉSTAMOS ===\n")
            print("1. Crear préstamo")
            print("2. Ver todos los préstamos")
            print("3. Ver préstamos activos")
            print("4. Ver préstamos de un usuario")
            print("5. Devolver libro")
            print("6. Ver préstamos retrasados")
            print("7. Renovar préstamo")
            print("0. Volver")
            
            opcion = input("\nSeleccione opción: ").strip()
            
            if opcion == "1":
                self._crear_prestamo()
            elif opcion == "2":
                self._ver_prestamos()
            elif opcion == "3":
                self._ver_prestamos_activos()
            elif opcion == "4":
                self._ver_prestamos_usuario()
            elif opcion == "5":
                self._devolver_libro()
            elif opcion == "6":
                self._ver_prestamos_retrasados()
            elif opcion == "7":
                self._renovar_prestamo()
            elif opcion == "0":
                break
            else:
                input("Opción inválida. Presione Enter para continuar...")
    
    def _crear_prestamo(self):
        """Crea un nuevo préstamo"""
        self.limpiar_pantalla()
        print("=== CREAR PRÉSTAMO ===\n")
        
        id_usuario = input("ID del usuario: ").strip()
        if not id_usuario.isdigit():
            print("ID de usuario inválido")
            input("Presione Enter para continuar...")
            return
        
        id_libro = input("ID del libro: ").strip()
        if not id_libro.isdigit():
            print("ID de libro inválido")
            input("Presione Enter para continuar...")
            return
        
        dias = input("Días de préstamo [14]: ").strip() or "14"
        
        try:
            dias = int(dias)
            id_prestamo = self.prestamos.crear_prestamo(int(id_usuario), int(id_libro), dias)
            if id_prestamo:
                print(f"\n✓ Préstamo creado exitosamente con ID {id_prestamo}")
            else:
                print("\n✗ No se pudo crear el préstamo")
        except ValueError:
            print("\n✗ Número de días inválido")
        except Exception as e:
            print(f"\n✗ Error: {e}")
        
        input("Presione Enter para continuar...")
    
    def _ver_prestamos(self):
        """Muestra todos los préstamos"""
        self.limpiar_pantalla()
        print("=== LISTA DE PRÉSTAMOS ===\n")
        
        try:
            prestamos = self.prestamos.obtener_todos_prestamos()
            if not prestamos:
                print("No hay préstamos registrados")
            else:
                print(f"{'ID':<5} {'Usuario':<20} {'Libro':<25} {'Estado':<10}")
                print("-" * 60)
                for prestamo in prestamos:
                    print(f"{prestamo['id']:<5} {prestamo['usuario_nombre']:<20} {prestamo['libro_titulo']:<25} {prestamo['estado']:<10}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _ver_prestamos_activos(self):
        """Muestra solo préstamos activos"""
        self.limpiar_pantalla()
        print("=== PRÉSTAMOS ACTIVOS ===\n")
        
        try:
            prestamos = self.prestamos.obtener_prestamos_activos()
            if not prestamos:
                print("No hay préstamos activos")
            else:
                print(f"{'ID':<5} {'Usuario':<20} {'Libro':<25} {'Devolución':<15}")
                print("-" * 65)
                for prestamo in prestamos:
                    print(f"{prestamo['id']:<5} {prestamo['usuario_nombre']:<20} {prestamo['libro_titulo']:<25} {prestamo['fecha_devolucion_esperada']:<15}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _ver_prestamos_usuario(self):
        """Ve préstamos de un usuario"""
        self.limpiar_pantalla()
        print("=== PRÉSTAMOS DE UN USUARIO ===\n")
        
        id_usuario = input("Ingrese el ID del usuario: ").strip()
        if not id_usuario.isdigit():
            print("ID inválido")
            input("Presione Enter para continuar...")
            return
        
        try:
            prestamos = self.prestamos.obtener_prestamos_usuario(int(id_usuario))
            if not prestamos:
                print("No hay préstamos para este usuario")
            else:
                print(f"\n{'ID':<5} {'Libro':<25} {'Estado':<10} {'Devolución':<15}")
                print("-" * 55)
                for prestamo in prestamos:
                    print(f"{prestamo['id']:<5} {prestamo['libro_titulo']:<25} {prestamo['estado']:<10} {prestamo['fecha_devolucion_esperada']:<15}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _devolver_libro(self):
        """Registra la devolución de un libro"""
        self.limpiar_pantalla()
        print("=== DEVOLVER LIBRO ===\n")
        
        id_prestamo = input("Ingrese el ID del préstamo: ").strip()
        if not id_prestamo.isdigit():
            print("ID inválido")
            input("Presione Enter para continuar...")
            return
        
        try:
            resultado = self.prestamos.devolver_libro(int(id_prestamo))
            if resultado:
                print(f"\n✓ Libro devuelto exitosamente")
                print(f"  Días de retraso: {resultado['dias_retraso']}")
                print(f"  Multa: ${resultado['multa']:.2f}")
            else:
                print("\n✗ No se pudo procesar la devolución")
        except Exception as e:
            print(f"\n✗ Error: {e}")
        
        input("Presione Enter para continuar...")
    
    def _ver_prestamos_retrasados(self):
        """Muestra préstamos retrasados"""
        self.limpiar_pantalla()
        print("=== PRÉSTAMOS RETRASADOS ===\n")
        
        try:
            prestamos = self.prestamos.obtener_prestamos_retrasados()
            if not prestamos:
                print("No hay préstamos retrasados")
            else:
                print(f"{'ID':<5} {'Usuario':<20} {'Libro':<25} {'Días Retraso':<15}")
                print("-" * 65)
                for prestamo in prestamos:
                    print(f"{prestamo['id']:<5} {prestamo['usuario_nombre']:<20} {prestamo['libro_titulo']:<25} {prestamo['dias_retraso']:<15}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _renovar_prestamo(self):
        """Renueva un préstamo"""
        self.limpiar_pantalla()
        print("=== RENOVAR PRÉSTAMO ===\n")
        
        id_prestamo = input("Ingrese el ID del préstamo: ").strip()
        if not id_prestamo.isdigit():
            print("ID inválido")
            input("Presione Enter para continuar...")
            return
        
        dias = input("Días de renovación [14]: ").strip() or "14"
        
        try:
            dias = int(dias)
            if self.prestamos.renovar_prestamo(int(id_prestamo), dias):
                print(f"\n✓ Préstamo renovado exitosamente")
            else:
                print("\n✗ No se pudo renovar el préstamo")
        except ValueError:
            print("\n✗ Número de días inválido")
        except Exception as e:
            print(f"\n✗ Error: {e}")
        
        input("Presione Enter para continuar...")
    
    def menu_reportes(self):
        """Menú de reportes"""
        while True:
            self.limpiar_pantalla()
            print("=== REPORTES ===\n")
            print("1. Estadísticas generales")
            print("2. Top 5 libros más prestados")
            print("3. Usuarios con préstamos activos")
            print("4. Libros con bajo stock")
            print("0. Volver")
            
            opcion = input("\nSeleccione opción: ").strip()
            
            if opcion == "1":
                self._estadisticas()
            elif opcion == "2":
                self._top_libros_prestados()
            elif opcion == "3":
                self._usuarios_con_prestamos()
            elif opcion == "4":
                self._libros_bajo_stock()
            elif opcion == "0":
                break
            else:
                input("Opción inválida. Presione Enter para continuar...")
    
    def _estadisticas(self):
        """Muestra estadísticas generales"""
        self.limpiar_pantalla()
        print("=== ESTADÍSTICAS GENERALES ===\n")
        
        try:
            autores = self.autores.obtener_todos_autores()
            libros = self.libros.obtener_todos_libros()
            usuarios = self.usuarios.obtener_todos_usuarios()
            prestamos_activos = self.prestamos.obtener_prestamos_activos()
            
            print(f"Total de autores: {len(autores)}")
            print(f"Total de libros: {len(libros)}")
            print(f"Total de usuarios: {len(usuarios)}")
            print(f"Préstamos activos: {len(prestamos_activos)}")
            
            # Libros disponibles
            libros_disp = sum(1 for l in libros if l['cantidad_disponible'] > 0)
            print(f"Libros con disponibilidad: {libros_disp}")
            
            # Usuarios activos
            usuarios_activos = sum(1 for u in usuarios if u['estado'] == 'activo')
            print(f"Usuarios activos: {usuarios_activos}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _top_libros_prestados(self):
        """Muestra top 5 libros más prestados"""
        self.limpiar_pantalla()
        print("=== TOP 5 LIBROS MÁS PRESTADOS ===\n")
        
        try:
            prestamos = self.prestamos.obtener_todos_prestamos()
            if not prestamos:
                print("No hay préstamos registrados")
            else:
                # Contar préstamos por libro
                conteo = {}
                for p in prestamos:
                    libro = p['libro_titulo']
                    conteo[libro] = conteo.get(libro, 0) + 1
                
                # Ordenar y tomar top 5
                top5 = sorted(conteo.items(), key=lambda x: x[1], reverse=True)[:5]
                
                print(f"{'Posición':<5} {'Libro':<40} {'Préstamos':<10}")
                print("-" * 55)
                for i, (libro, count) in enumerate(top5, 1):
                    print(f"{i:<5} {libro:<40} {count:<10}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _usuarios_con_prestamos(self):
        """Muestra usuarios con préstamos activos"""
        self.limpiar_pantalla()
        print("=== USUARIOS CON PRÉSTAMOS ACTIVOS ===\n")
        
        try:
            prestamos = self.prestamos.obtener_prestamos_activos()
            if not prestamos:
                print("No hay préstamos activos")
            else:
                usuarios_set = {}
                for p in prestamos:
                    usuario = p['usuario_nombre']
                    usuarios_set[usuario] = usuarios_set.get(usuario, 0) + 1
                
                print(f"{'Usuario':<30} {'Préstamos':<10}")
                print("-" * 40)
                for usuario, count in usuarios_set.items():
                    print(f"{usuario:<30} {count:<10}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _libros_bajo_stock(self):
        """Muestra libros con bajo stock"""
        self.limpiar_pantalla()
        print("=== LIBROS CON BAJO STOCK ===\n")
        
        try:
            libros = self.libros.obtener_todos_libros()
            libros_bajo_stock = [l for l in libros if l['cantidad_disponible'] <= 1]
            
            if not libros_bajo_stock:
                print("No hay libros con bajo stock")
            else:
                print(f"{'Título':<30} {'Disponibles':<15} {'Total':<10}")
                print("-" * 55)
                for libro in libros_bajo_stock:
                    print(f"{libro['titulo']:<30} {libro['cantidad_disponible']:<15} {libro['cantidad_total']:<10}")
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def ejecutar(self):
        """Inicia el programa principal"""
        while True:
            self.mostrar_menu_principal()
            opcion = input("Seleccione opción: ").strip()
            
            if opcion == "1":
                self.menu_autores()
            elif opcion == "2":
                self.menu_libros()
            elif opcion == "3":
                self.menu_usuarios()
            elif opcion == "4":
                self.menu_prestamos()
            elif opcion == "5":
                self.menu_reportes()
            elif opcion == "0":
                print("\n¡Gracias por usar el Sistema de Gestión de Biblioteca!")
                self.db.cerrar()
                break
            else:
                input("Opción inválida. Presione Enter para continuar...")


def main():
    """Función principal"""
    sistema = SistemaBiblioteca()
    sistema.ejecutar()


if __name__ == "__main__":
    main()
