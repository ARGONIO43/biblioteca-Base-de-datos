"""
Módulo de gestión de usuarios
CRUD para crear, leer, actualizar y eliminar usuarios
"""

import logging
from db import BaseDatos

logger = logging.getLogger(__name__)


class GestorUsuarios:
    """Gestiona las operaciones CRUD de usuarios"""
    
    def __init__(self, base_datos):
        """Inicializa el gestor con una instancia de base de datos"""
        self.db = base_datos
    
    def agregar_usuario(self, nombre, email, telefono=None, direccion=None, tipo_usuario="estudiante"):
        """
        Agrega un nuevo usuario a la base de datos
        
        Args:
            nombre (str): Nombre del usuario
            email (str): Email único del usuario
            telefono (str): Teléfono del usuario
            direccion (str): Dirección del usuario
            tipo_usuario (str): Tipo de usuario (estudiante, docente, administrativo)
            
        Returns:
            int: ID del usuario creado
        """
        try:
            query = '''
                INSERT INTO usuarios (nombre, email, telefono, direccion, tipo_usuario)
                VALUES (?, ?, ?, ?, ?)
            '''
            id_usuario = self.db.ejecutar(query, (nombre, email, telefono, direccion, tipo_usuario))
            logger.info(f"Usuario '{nombre}' agregado con ID {id_usuario}")
            return id_usuario
        except Exception as e:
            logger.error(f"Error al agregar usuario: {e}")
            raise
    
    def obtener_usuario(self, id_usuario):
        """Obtiene información de un usuario por su ID"""
        try:
            query = 'SELECT * FROM usuarios WHERE id = ?'
            resultado = self.db.consultar_uno(query, (id_usuario,))
            if resultado:
                return dict(resultado)
            logger.warning(f"Usuario con ID {id_usuario} no encontrado")
            return None
        except Exception as e:
            logger.error(f"Error al obtener usuario: {e}")
            raise
    
    def obtener_todos_usuarios(self):
        """Obtiene todos los usuarios"""
        try:
            query = 'SELECT * FROM usuarios ORDER BY nombre'
            resultados = self.db.consultar(query)
            return [dict(fila) for fila in resultados]
        except Exception as e:
            logger.error(f"Error al obtener usuarios: {e}")
            raise
    
    def obtener_por_email(self, email):
        """Busca un usuario por email"""
        try:
            query = 'SELECT * FROM usuarios WHERE email = ?'
            resultado = self.db.consultar_uno(query, (email,))
            if resultado:
                return dict(resultado)
            return None
        except Exception as e:
            logger.error(f"Error al obtener usuario por email: {e}")
            raise
    
    def buscar_usuario(self, nombre):
        """Busca usuarios por nombre (búsqueda parcial)"""
        try:
            query = "SELECT * FROM usuarios WHERE nombre LIKE ? ORDER BY nombre"
            resultados = self.db.consultar(query, (f"%{nombre}%",))
            return [dict(fila) for fila in resultados]
        except Exception as e:
            logger.error(f"Error al buscar usuario: {e}")
            raise
    
    def obtener_por_tipo(self, tipo_usuario):
        """Obtiene usuarios por tipo"""
        try:
            query = 'SELECT * FROM usuarios WHERE tipo_usuario = ? ORDER BY nombre'
            resultados = self.db.consultar(query, (tipo_usuario,))
            return [dict(fila) for fila in resultados]
        except Exception as e:
            logger.error(f"Error al obtener usuarios por tipo: {e}")
            raise
    
    def actualizar_usuario(self, id_usuario, **kwargs):
        """
        Actualiza información de un usuario
        
        Args:
            id_usuario (int): ID del usuario
            **kwargs: Campos a actualizar
        """
        try:
            campos_permitidos = ['nombre', 'email', 'telefono', 'direccion', 'tipo_usuario', 'estado']
            campos = {k: v for k, v in kwargs.items() if k in campos_permitidos}
            
            if not campos:
                logger.warning("No hay campos válidos para actualizar")
                return False
            
            set_clause = ', '.join([f"{k} = ?" for k in campos.keys()])
            query = f'UPDATE usuarios SET {set_clause} WHERE id = ?'
            valores = list(campos.values()) + [id_usuario]
            
            self.db.ejecutar(query, valores)
            logger.info(f"Usuario {id_usuario} actualizado")
            return True
        except Exception as e:
            logger.error(f"Error al actualizar usuario: {e}")
            raise
    
    def eliminar_usuario(self, id_usuario):
        """
        Elimina un usuario de la base de datos
        
        Args:
            id_usuario (int): ID del usuario
            
        Returns:
            bool: True si se eliminó, False si no existe
        """
        try:
            usuario = self.obtener_usuario(id_usuario)
            if not usuario:
                logger.warning(f"Usuario {id_usuario} no existe")
                return False
            
            query = 'DELETE FROM usuarios WHERE id = ?'
            self.db.ejecutar(query, (id_usuario,))
            logger.info(f"Usuario {id_usuario} eliminado")
            return True
        except Exception as e:
            logger.error(f"Error al eliminar usuario: {e}")
            raise
    
    def cambiar_estado(self, id_usuario, nuevo_estado):
        """
        Cambia el estado del usuario (activo/inactivo)
        
        Args:
            id_usuario (int): ID del usuario
            nuevo_estado (str): Nuevo estado (activo/inactivo)
            
        Returns:
            bool: True si se cambió
        """
        try:
            if nuevo_estado not in ['activo', 'inactivo']:
                logger.warning(f"Estado inválido: {nuevo_estado}")
                return False
            
            query = 'UPDATE usuarios SET estado = ? WHERE id = ?'
            self.db.ejecutar(query, (nuevo_estado, id_usuario))
            logger.info(f"Estado del usuario {id_usuario} cambió a {nuevo_estado}")
            return True
        except Exception as e:
            logger.error(f"Error al cambiar estado: {e}")
            raise
    
    def obtener_activos(self):
        """Obtiene solo los usuarios activos"""
        try:
            query = 'SELECT * FROM usuarios WHERE estado = "activo" ORDER BY nombre'
            resultados = self.db.consultar(query)
            return [dict(fila) for fila in resultados]
        except Exception as e:
            logger.error(f"Error al obtener usuarios activos: {e}")
            raise
