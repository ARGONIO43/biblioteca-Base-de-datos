"""
Módulo de gestión de libros
CRUD para crear, leer, actualizar y eliminar libros
"""

import logging
from db import BaseDatos

logger = logging.getLogger(__name__)


class GestorLibros:
    """Gestiona las operaciones CRUD de libros"""
    
    def __init__(self, base_datos):
        """Inicializa el gestor con una instancia de base de datos"""
        self.db = base_datos
    
    def agregar_libro(self, titulo, id_autor, isbn, año_publicacion=None, 
                     editorial=None, categoria=None, cantidad_total=1, descripcion=None):
        """
        Agrega un nuevo libro a la base de datos
        
        Args:
            titulo (str): Título del libro
            id_autor (int): ID del autor
            isbn (str): ISBN único del libro
            año_publicacion (int): Año de publicación
            editorial (str): Editorial del libro
            categoria (str): Categoría del libro
            cantidad_total (int): Cantidad total de ejemplares
            descripcion (str): Descripción del libro
            
        Returns:
            int: ID del libro creado
        """
        try:
            query = '''
                INSERT INTO libros 
                (titulo, id_autor, isbn, año_publicacion, editorial, categoria, 
                 cantidad_total, cantidad_disponible, descripcion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            id_libro = self.db.ejecutar(query, (
                titulo, id_autor, isbn, año_publicacion, editorial, categoria,
                cantidad_total, cantidad_total, descripcion
            ))
            logger.info(f"Libro '{titulo}' agregado con ID {id_libro}")
            return id_libro
        except Exception as e:
            logger.error(f"Error al agregar libro: {e}")
            raise
    
    def obtener_libro(self, id_libro):
        """Obtiene información de un libro por su ID"""
        try:
            query = '''
                SELECT l.*, a.nombre as autor_nombre
                FROM libros l
                LEFT JOIN autores a ON l.id_autor = a.id
                WHERE l.id = ?
            '''
            resultado = self.db.consultar_uno(query, (id_libro,))
            if resultado:
                return dict(resultado)
            logger.warning(f"Libro con ID {id_libro} no encontrado")
            return None
        except Exception as e:
            logger.error(f"Error al obtener libro: {e}")
            raise
    
    def obtener_todos_libros(self):
        """Obtiene todos los libros con información del autor"""
        try:
            query = '''
                SELECT l.*, a.nombre as autor_nombre
                FROM libros l
                LEFT JOIN autores a ON l.id_autor = a.id
                ORDER BY l.titulo
            '''
            resultados = self.db.consultar(query)
            return [dict(fila) for fila in resultados]
        except Exception as e:
            logger.error(f"Error al obtener libros: {e}")
            raise
    
    def buscar_libro(self, termino):
        """Busca libros por título, ISBN o categoría"""
        try:
            query = '''
                SELECT l.*, a.nombre as autor_nombre
                FROM libros l
                LEFT JOIN autores a ON l.id_autor = a.id
                WHERE l.titulo LIKE ? OR l.isbn LIKE ? OR l.categoria LIKE ?
                ORDER BY l.titulo
            '''
            termino_busqueda = f"%{termino}%"
            resultados = self.db.consultar(query, (termino_busqueda, termino_busqueda, termino_busqueda))
            return [dict(fila) for fila in resultados]
        except Exception as e:
            logger.error(f"Error al buscar libro: {e}")
            raise
    
    def obtener_por_categoria(self, categoria):
        """Obtiene todos los libros de una categoría"""
        try:
            query = '''
                SELECT l.*, a.nombre as autor_nombre
                FROM libros l
                LEFT JOIN autores a ON l.id_autor = a.id
                WHERE l.categoria = ?
                ORDER BY l.titulo
            '''
            resultados = self.db.consultar(query, (categoria,))
            return [dict(fila) for fila in resultados]
        except Exception as e:
            logger.error(f"Error al obtener libros por categoría: {e}")
            raise
    
    def actualizar_libro(self, id_libro, **kwargs):
        """
        Actualiza información de un libro
        
        Args:
            id_libro (int): ID del libro
            **kwargs: Campos a actualizar
        """
        try:
            campos_permitidos = ['titulo', 'isbn', 'año_publicacion', 'editorial', 
                               'categoria', 'cantidad_total', 'descripcion']
            campos = {k: v for k, v in kwargs.items() if k in campos_permitidos}
            
            if not campos:
                logger.warning("No hay campos válidos para actualizar")
                return False
            
            set_clause = ', '.join([f"{k} = ?" for k in campos.keys()])
            query = f'UPDATE libros SET {set_clause} WHERE id = ?'
            valores = list(campos.values()) + [id_libro]
            
            self.db.ejecutar(query, valores)
            logger.info(f"Libro {id_libro} actualizado")
            return True
        except Exception as e:
            logger.error(f"Error al actualizar libro: {e}")
            raise
    
    def eliminar_libro(self, id_libro):
        """
        Elimina un libro de la base de datos
        
        Args:
            id_libro (int): ID del libro
            
        Returns:
            bool: True si se eliminó, False si no existe
        """
        try:
            libro = self.obtener_libro(id_libro)
            if not libro:
                logger.warning(f"Libro {id_libro} no existe")
                return False
            
            query = 'DELETE FROM libros WHERE id = ?'
            self.db.ejecutar(query, (id_libro,))
            logger.info(f"Libro {id_libro} eliminado")
            return True
        except Exception as e:
            logger.error(f"Error al eliminar libro: {e}")
            raise
    
    def obtener_disponibles(self):
        """Obtiene solo los libros con ejemplares disponibles"""
        try:
            query = '''
                SELECT l.*, a.nombre as autor_nombre
                FROM libros l
                LEFT JOIN autores a ON l.id_autor = a.id
                WHERE l.cantidad_disponible > 0
                ORDER BY l.titulo
            '''
            resultados = self.db.consultar(query)
            return [dict(fila) for fila in resultados]
        except Exception as e:
            logger.error(f"Error al obtener libros disponibles: {e}")
            raise
    
    def actualizar_disponibilidad(self, id_libro, cambio):
        """
        Actualiza la cantidad disponible de un libro
        
        Args:
            id_libro (int): ID del libro
            cambio (int): Cambio en la cantidad (positivo o negativo)
            
        Returns:
            bool: True si se actualizó, False si no hay suficientes ejemplares
        """
        try:
            libro = self.obtener_libro(id_libro)
            if not libro:
                logger.warning(f"Libro {id_libro} no existe")
                return False
            
            nueva_cantidad = libro['cantidad_disponible'] + cambio
            
            if nueva_cantidad < 0:
                logger.warning(f"Cantidad disponible insuficiente para libro {id_libro}")
                return False
            
            query = 'UPDATE libros SET cantidad_disponible = ? WHERE id = ?'
            self.db.ejecutar(query, (nueva_cantidad, id_libro))
            logger.info(f"Disponibilidad del libro {id_libro} actualizada a {nueva_cantidad}")
            return True
        except Exception as e:
            logger.error(f"Error al actualizar disponibilidad: {e}")
            raise
