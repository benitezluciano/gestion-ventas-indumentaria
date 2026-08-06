import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "ventas.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def inicializar_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS categorias (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre  TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS productos (
            id             TEXT PRIMARY KEY,
            nombre         TEXT NOT NULL,
            categoria_id   INTEGER NOT NULL,
            precio_costo   REAL NOT NULL,
            precio_venta   REAL NOT NULL,
            talle          TEXT,
            color          TEXT,
            stock          INTEGER NOT NULL DEFAULT 0,
            stock_minimo   INTEGER NOT NULL DEFAULT 0,
            activo         INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        );

        CREATE TABLE IF NOT EXISTS ventas (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha               TEXT NOT NULL,
            total               REAL NOT NULL,
            descuento           REAL NOT NULL DEFAULT 0,
            estado              TEXT NOT NULL DEFAULT 'Completada',
            motivo_cancelacion  TEXT
        );

        CREATE TABLE IF NOT EXISTS detalle_venta (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id        INTEGER NOT NULL,
            producto_id     TEXT NOT NULL,
            cantidad        INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            subtotal        REAL NOT NULL,
            FOREIGN KEY (venta_id)    REFERENCES ventas(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        );
    """)

    conn.commit()
    conn.close()