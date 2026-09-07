"""
Módulo de gestión de préstamos
CRUD para crear, leer, actualizar y eliminar préstamos
Calcula multas por retrasos
"""

import logging
from datetime import datetime, timedelta
from db import BaseDatos

logger = logging.getLogger(__name__)


class GestorPrestamos:
    """Gestiona las operaciones CRUD de préstamos y cálculo de multas"""
    
    DIAS_PRESTAMO_DEFAULT = 14  # Días por defecto para un préstamo
    MULTA_DIARIA = 10.0  # Multa diaria en pesos
    
    def __init__(self, base_datos):
        """Inicializa el gestor con una instancia de base de datos"""
        self.db = base_datos
    
    def crear_prestamo(self, id_usuario, id_libro, dias_prestamo=None):
        """
        Crea un nuevo préstamo
        
        Args:
            id_usuario (int): ID del usuario
            id_libro (int): ID del libro
            dias_prestamo (int): Número de días para el préstamo
            
        Returns:
            int: ID del préstamo creado, o None si hay error
        """
        try:
            if dias_prestamo is None:
                dias_prestamo = self.DIAS_PRESTAMO_DEFAULT
            
            # Verificar que el usuario existe y está activo
            usuario = self.db.consultar_uno('SELECT * FROM usuarios WHERE id = ? AND estado = "activo"', (id_usuario,))
            if not usuario:
                logger.warning(f"Usuario {id_usuario} no existe o está inactivo")
                return None
            
            # Verificar que el libro existe y hay ejemplares disponibles
            libro = self.db.consultar_uno('SELECT * FROM libros WHERE id = ?', (id_libro,))
            if not libro:
                logger.warning(f"Libro {id_libro} no existe")
                return None
            
            if libro['cantidad_disponible'] <= 0:
                logger.warning(f"No hay ejemplares disponibles del libro {id_libro}")
                return None
            
            # Calcular fecha de devolución esperada
            fecha_prestamo = datetime.now()
            fecha_devolucion = fecha_prestamo + timedelta(days=dias_prestamo)
            
            # Crear préstamo
            query = '''
                INSERT INTO prestamos 
                (id_usuario, id_libro, fecha_devolucion_esperada, estado)
                VALUES (?, ?, ?, 'activo')
            '''
            id_prestamo = self.db.ejecutar(query, (
                id_usuario, id_libro, fecha_devolucion.date()
            ))
            
            # Actualizar disponibilidad del libro (importar aquí para evitar circular imports)
            from libros import GestorLibros
            gestor_libros = GestorLibros(self.db)
            gestor_libros.actualizar_disponibilidad(id_libro, -1)
            
            logger.info(f"Préstamo {id_prestamo} creado: usuario {id_usuario}, libro {id_libro}")
            return id_prestamo
        except Exception as e:
            logger.error(f"Error al crear préstamo: {e}")
            raise
    
    def obtener_prestamo(self, id_prestamo):
        """Obtiene información de un préstamo"""
        try:
            query = '''
                SELECT p.*, u.nombre as usuario_nombre, l.titulo as libro_titulo
                FROM prestamos p
                LEFT JOIN usuarios u ON p.id_usuario = u.id
                LEFT JOIN libros l ON p.id_libro = l.id
                WHERE p.id = ?
            '''
            resultado = self.db.consultar_uno(query, (id_prestamo,))
            if resultado:
                return dict(resultado)
            logger.warning(f"Préstamo {id_prestamo} no encontrado")
            return None
        except Exception as e:
            logger.error(f"Error al obtener préstamo: {e}")
            raise
    
    def obtener_todos_prestamos(self):
        """Obtiene todos los préstamos"""
        try:
            query = '''
                SELECT p.*, u.nombre as usuario_nombre, l.titulo as libro_titulo
                FROM prestamos p
                LEFT JOIN usuarios u ON p.id_usuario = u.id
                LEFT JOIN libros l ON p.id_libro = l.id
                ORDER BY p.fecha_prestamo DESC
            '''
            resultados = self.db.consultar(query)
            return [dict(fila) for fila in resultados]
        except Exception as e:
            logger.error(f"Error al obtener préstamos: {e}")
            raise
    
    def obtener_prestamos_activos(self):
        """Obtiene solo los préstamos activos (no devueltos)"""
        try:
            query = '''
                SELECT p.*, u.nombre as usuario_nombre, l.titulo as libro_titulo
                FROM prestamos p
                LEFT JOIN usuarios u ON p.id_usuario = u.id
                LEFT JOIN libros l ON p.id_libro = l.id
                WHERE p.estado = 'activo'
                ORDER BY p.fecha_devolucion_esperada
            '''
            resultados = self.db.consultar(query)
            return [dict(fila) for fila in resultados]
        except Exception as e:
            logger.error(f"Error al obtener préstamos activos: {e}")
            raise
    
    def obtener_prestamos_usuario(self, id_usuario):
        """Obtiene todos los préstamos de un usuario"""
        try:
            query = '''
                SELECT p.*, l.titulo as libro_titulo
                FROM prestamos p
                LEFT JOIN libros l ON p.id_libro = l.id
                WHERE p.id_usuario = ?
                ORDER BY p.fecha_prestamo DESC
            '''
            resultados = self.db.consultar(query, (id_usuario,))
            return [dict(fila) for fila in resultados]
        except Exception as e:
            logger.error(f"Error al obtener préstamos del usuario: {e}")
            raise
    
    def obtener_prestamos_libro(self, id_libro):
        """Obtiene todos los préstamos de un libro"""
        try:
            query = '''
                SELECT p.*, u.nombre as usuario_nombre
                FROM prestamos p
                LEFT JOIN usuarios u ON p.id_usuario = u.id
                WHERE p.id_libro = ?
                ORDER BY p.fecha_prestamo DESC
            '''
            resultados = self.db.consultar(query, (id_libro,))
            return [dict(fila) for fila in resultados]
        except Exception as e:
            logger.error(f"Error al obtener préstamos del libro: {e}")
            raise
    
    def devolver_libro(self, id_prestamo):
        """
        Registra la devolución de un libro y calcula multa si es necesario
        
        Args:
            id_prestamo (int): ID del préstamo
            
        Returns:
            dict: Información de la devolución incluyendo multa calculada
        """
        try:
            prestamo = self.obtener_prestamo(id_prestamo)
            if not prestamo:
                logger.warning(f"Préstamo {id_prestamo} no existe")
                return None
            
            if prestamo['estado'] != 'activo':
                logger.warning(f"Préstamo {id_prestamo} no está activo")
                return None
            
            # Calcular multa por retraso
            fecha_devolucion = datetime.now().date()
            fecha_esperada = datetime.strptime(prestamo['fecha_devolucion_esperada'], '%Y-%m-%d').date()
            dias_retraso = (fecha_devolucion - fecha_esperada).days
            
            multa = 0.0
            if dias_retraso > 0:
                multa = dias_retraso * self.MULTA_DIARIA
                logger.info(f"Multa calculada: {dias_retraso} días × ${self.MULTA_DIARIA} = ${multa}")
            
            # Actualizar préstamo
            query = '''
                UPDATE prestamos 
                SET estado = 'devuelto', fecha_devolucion_real = ?, multa = ?
                WHERE id = ?
            '''
            self.db.ejecutar(query, (fecha_devolucion, multa, id_prestamo))
            
            # Devolver disponibilidad del libro
            from libros import GestorLibros
            gestor_libros = GestorLibros(self.db)
            gestor_libros.actualizar_disponibilidad(prestamo['id_libro'], 1)
            
            logger.info(f"Libro devuelto. Préstamo {id_prestamo}, multa: ${multa}")
            
            return {
                'id_prestamo': id_prestamo,
                'fecha_devolucion': fecha_devolucion,
                'dias_retraso': max(0, dias_retraso),
                'multa': multa
            }
        except Exception as e:
            logger.error(f"Error al devolver libro: {e}")
            raise
    
    def obtener_prestamos_retrasados(self):
        """Obtiene préstamos que están retrasados"""
        try:
            hoy = datetime.now().date()
            query = '''
                SELECT p.*, u.nombre as usuario_nombre, l.titulo as libro_titulo,
                       CAST((julianday(?) - julianday(p.fecha_devolucion_esperada)) AS INTEGER) as dias_retraso
                FROM prestamos p
                LEFT JOIN usuarios u ON p.id_usuario = u.id
                LEFT JOIN libros l ON p.id_libro = l.id
                WHERE p.estado = 'activo' AND p.fecha_devolucion_esperada < ?
                ORDER BY p.fecha_devolucion_esperada
            '''
            resultados = self.db.consultar(query, (str(hoy), str(hoy)))
            return [dict(fila) for fila in resultados]
        except Exception as e:
            logger.error(f"Error al obtener préstamos retrasados: {e}")
            raise
    
    def renovar_prestamo(self, id_prestamo, dias_renovacion=None):
        """
        Renueva la fecha de devolución de un préstamo
        
        Args:
            id_prestamo (int): ID del préstamo
            dias_renovacion (int): Días adicionales de prórroga
            
        Returns:
            bool: True si se renovó, False si no es posible
        """
        try:
            if dias_renovacion is None:
                dias_renovacion = self.DIAS_PRESTAMO_DEFAULT
            
            prestamo = self.obtener_prestamo(id_prestamo)
            if not prestamo:
                logger.warning(f"Préstamo {id_prestamo} no existe")
                return False
            
            if prestamo['estado'] != 'activo':
                logger.warning(f"Préstamo {id_prestamo} no está activo")
                return False
            
            # Calcular nueva fecha
            fecha_actual_esperada = datetime.strptime(prestamo['fecha_devolucion_esperada'], '%Y-%m-%d')
            nueva_fecha = fecha_actual_esperada + timedelta(days=dias_renovacion)
            
            query = 'UPDATE prestamos SET fecha_devolucion_esperada = ? WHERE id = ?'
            self.db.ejecutar(query, (nueva_fecha.date(), id_prestamo))
            
            logger.info(f"Préstamo {id_prestamo} renovado hasta {nueva_fecha.date()}")
            return True
        except Exception as e:
            logger.error(f"Error al renovar préstamo: {e}")
            raise
