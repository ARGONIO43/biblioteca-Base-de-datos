"""
Módulo de gestión de autores
CRUD para crear, leer, actualizar y eliminar autores
"""

import logging
from db import BaseDatos

logger = logging.getLogger(__name__)


class GestorAutores:
    """Gestiona las operaciones CRUD de autores"""
    
    def __init__(self, base_datos):
        """Inicializa el gestor con una instancia de base de datos"""
        self.db = base_datos
    
    def agregar_autor(self, nombre, fecha_nacimiento=None, nacionalidad=None, biografia=None):
        """
        Agrega un nuevo autor a la base de datos
        
        Args:
            nombre (str): Nombre del autor
            fecha_nacimiento (str): Fecha de nacimiento (YYYY-MM-DD)
            nacionalidad (str): Nacionalidad del autor
            biografia (str): Biografía del autor
            
        Returns:
            int: ID del autor creado
        """
        try:
            query = '''
                INSERT INTO autores (nombre, fecha_nacimiento, nacionalidad, biografia)
                VALUES (?, ?, ?, ?)
            '''
            id_autor = self.db.ejecutar(query, (nombre, fecha_nacimiento, nacionalidad, biografia))
            logger.info(f"Autor '{nombre}' agregado con ID {id_autor}")
            return id_autor
        except Exception as e:
            logger.error(f"Error al agregar autor: {e}")
            raise
    
    def obtener_autor(self, id_autor):
        """Obtiene información de un autor por su ID"""
        try:
            query = 'SELECT * FROM autores WHERE id = ?'
            resultado = self.db.consultar_uno(query, (id_autor,))
            if resultado:
                return dict(resultado)
            logger.warning(f"Autor con ID {id_autor} no encontrado")
            return None
        except Exception as e:
            logger.error(f"Error al obtener autor: {e}")
            raise
    
    def obtener_todos_autores(self):
        """Obtiene todos los autores"""
        try:
            query = 'SELECT * FROM autores ORDER BY nombre'
            resultados = self.db.consultar(query)
            return [dict(fila) for fila in resultados]
        except Exception as e:
            logger.error(f"Error al obtener autores: {e}")
            raise
    
    def buscar_autor(self, nombre):
        """Busca autores por nombre (búsqueda parcial)"""
        try:
            query = "SELECT * FROM autores WHERE nombre LIKE ? ORDER BY nombre"
            resultados = self.db.consultar(query, (f"%{nombre}%",))
            return [dict(fila) for fila in resultados]
        except Exception as e:
            logger.error(f"Error al buscar autor: {e}")
            raise
    
    def actualizar_autor(self, id_autor, **kwargs):
        """
        Actualiza información de un autor
        
        Args:
            id_autor (int): ID del autor
            **kwargs: Campos a actualizar (nombre, fecha_nacimiento, nacionalidad, biografia)
        """
        try:
            campos_permitidos = ['nombre', 'fecha_nacimiento', 'nacionalidad', 'biografia']
            campos = {k: v for k, v in kwargs.items() if k in campos_permitidos}
            
            if not campos:
                logger.warning("No hay campos válidos para actualizar")
                return False
            
            set_clause = ', '.join([f"{k} = ?" for k in campos.keys()])
            query = f'UPDATE autores SET {set_clause} WHERE id = ?'
            valores = list(campos.values()) + [id_autor]
            
            self.db.ejecutar(query, valores)
            logger.info(f"Autor {id_autor} actualizado")
            return True
        except Exception as e:
            logger.error(f"Error al actualizar autor: {e}")
            raise
    
    def eliminar_autor(self, id_autor):
        """
        Elimina un autor (también elimina sus libros asociados)
        
        Args:
            id_autor (int): ID del autor
            
        Returns:
            bool: True si se eliminó, False si no existe
        """
        try:
            autor = self.obtener_autor(id_autor)
            if not autor:
                logger.warning(f"Autor {id_autor} no existe")
                return False
            
            query = 'DELETE FROM autores WHERE id = ?'
            self.db.ejecutar(query, (id_autor,))
            logger.info(f"Autor {id_autor} eliminado")
            return True
        except Exception as e:
            logger.error(f"Error al eliminar autor: {e}")
            raise
    
    def obtener_libros_autor(self, id_autor):
        """Obtiene todos los libros de un autor"""
        try:
            query = '''
                SELECT l.id, l.titulo, l.isbn, l.año_publicacion, l.cantidad_disponible
                FROM libros l
                WHERE l.id_autor = ?
                ORDER BY l.año_publicacion DESC
            '''
            resultados = self.db.consultar(query, (id_autor,))
            return [dict(fila) for fila in resultados]
        except Exception as e:
            logger.error(f"Error al obtener libros del autor: {e}")
            raise
