"""
Módulo de gestión de base de datos SQLite
Maneja la conexión y creación de tablas relacional
"""

import sqlite3
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BaseDatos:
    """Gestiona la conexión y operaciones con la base de datos SQLite"""
    
    def __init__(self, nombre_db="biblioteca.db"):
        """Inicializa la conexión a la base de datos"""
        self.db_path = Path(nombre_db)
        self.conexion = None
        self.conectar()
        self.crear_tablas()
    
    def conectar(self):
        """Establece conexión con la base de datos"""
        try:
            self.conexion = sqlite3.connect(str(self.db_path))
            self.conexion.row_factory = sqlite3.Row  # Acceso por nombre de columna
            logger.info(f"Conexión establecida: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Error de conexión: {e}")
            raise
    
    def crear_tablas(self):
        """Crea las tablas de la base de datos si no existen"""
        cursor = self.conexion.cursor()
        
        try:
            # Tabla de autores
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS autores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    fecha_nacimiento DATE,
                    nacionalidad TEXT,
                    biografia TEXT,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de libros
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS libros (
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
                    FOREIGN KEY (id_autor) REFERENCES autores(id) ON DELETE CASCADE
                )
            ''')
            
            # Tabla de usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    telefono TEXT,
                    direccion TEXT,
                    tipo_usuario TEXT DEFAULT 'estudiante',
                    estado TEXT DEFAULT 'activo',
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de préstamos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prestamos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_usuario INTEGER NOT NULL,
                    id_libro INTEGER NOT NULL,
                    fecha_prestamo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_devolucion_esperada DATE NOT NULL,
                    fecha_devolucion_real DATE,
                    estado TEXT DEFAULT 'activo',
                    multa REAL DEFAULT 0.0,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE,
                    FOREIGN KEY (id_libro) REFERENCES libros(id) ON DELETE CASCADE
                )
            ''')
            
            self.conexion.commit()
            logger.info("Tablas creadas correctamente")
            
        except sqlite3.Error as e:
            logger.error(f"Error al crear tablas: {e}")
            raise
    
    def ejecutar(self, query, parametros=None):
        """Ejecuta una query de modificación (INSERT, UPDATE, DELETE)"""
        try:
            cursor = self.conexion.cursor()
            if parametros:
                cursor.execute(query, parametros)
            else:
                cursor.execute(query)
            self.conexion.commit()
            logger.debug(f"Query ejecutada: {query}")
            return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error ejecutando query: {e}")
            self.conexion.rollback()
            raise
    
    def consultar(self, query, parametros=None):
        """Ejecuta una query de consulta (SELECT) y retorna resultados"""
        try:
            cursor = self.conexion.cursor()
            if parametros:
                cursor.execute(query, parametros)
            else:
                cursor.execute(query)
            resultados = cursor.fetchall()
            logger.debug(f"Consulta ejecutada: {query}")
            return resultados
        except sqlite3.Error as e:
            logger.error(f"Error en consulta: {e}")
            raise
    
    def consultar_uno(self, query, parametros=None):
        """Ejecuta una query de consulta y retorna un solo resultado"""
        try:
            cursor = self.conexion.cursor()
            if parametros:
                cursor.execute(query, parametros)
            else:
                cursor.execute(query)
            resultado = cursor.fetchone()
            logger.debug(f"Consulta ejecutada: {query}")
            return resultado
        except sqlite3.Error as e:
            logger.error(f"Error en consulta: {e}")
            raise
    
    def cerrar(self):
        """Cierra la conexión a la base de datos"""
        if self.conexion:
            self.conexion.close()
            logger.info("Conexión cerrada")
