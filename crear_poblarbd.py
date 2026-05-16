# python crear_poblarbd.py

import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from sqlalchemy import create_engine, Column, Integer, String, Date, Text
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import declarative_base, sessionmaker
# pyrefly: ignore [missing-import]
from faker import Faker

# Cargar variables de entorno
load_dotenv()

# Configuración desde .env con validación y valores por defecto
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "test")

# Validar que el puerto sea un número entero válido
try:
    DB_PORT = int(DB_PORT)
except ValueError:
    print(f"Puerto inválido: {DB_PORT}, usando puerto 3306 por defecto")
    DB_PORT = 3306

# Construir URL de conexión MySQL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"Conectando a: {DB_HOST}:{DB_PORT}/{DB_NAME}")

# Crear motor de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)

# Base declarativa corregida para evitar el MovedIn20Warning
Base = declarative_base()

# Definir la tabla con nombre personalizado
class Personas_Juan(Base):
    __tablename__ = "personas_juan"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_completo = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    ciudad = Column(String(80), nullable=False)
    pais = Column(String(80), nullable=False)
    profesion = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    direccion = Column(Text, nullable=True)

# Función principal
def main():
    print("Conectando a la base de datos...")
    # Crear tablas si no existen
    Base.metadata.create_all(engine)
    print("Tabla verificada/creada exitosamente.")

    # Sesión
    Session = sessionmaker(bind=engine)
    session = Session()

    # Inicializar Faker en español de Colombia
    fake = Faker("es_CO")

    print("Generando 100,000 registros con Faker...")
    registros = []
    BATCH_SIZE = 5000  # Lotes controlados para no saturar la red ni max_allowed_packet

    for i in range(100000):
        email = fake.unique.email()
        
        # 1. Procesar y limpiar la dirección generada por Faker
        raw_address = fake.address()
        # Dividir por líneas para aislar los componentes
        partes = [p.strip() for p in raw_address.split('\n') if p.strip()]
        
        # La primera línea siempre contiene la nomenclatura de la calle
        direccion_limpia = partes[0] if partes else "Dirección desconocida"
        
        # 2. Extraer o generar una ciudad libre de códigos postales y saltos
        ciudad_limpia = fake.city()
        if len(partes) > 1:
            # Intenta obtener el municipio de la última línea (ej: "Urumita, La Guajira")
            ultima_linea = partes[-1]
            if ',' in ultima_linea:
                posible_ciudad = ultima_linea.split(',')[0].strip()
                # Verificar que no sea un número suelto o código postal residual
                if not posible_ciudad.isdigit() and len(posible_ciudad) > 2:
                    ciudad_limpia = posible_ciudad

        # 3. Limpiar caracteres raros en el número de teléfono
        telefono_limpio = fake.phone_number().replace(" ", "").replace("(", "").replace(")", "")

        registros.append({
            "nombre_completo": fake.name(),
            "email": email,
            "fecha_nacimiento": fake.date_of_birth(minimum_age=18, maximum_age=90),
            "ciudad": ciudad_limpia,
            "pais": "Colombia",
            "profesion": fake.job(),
            "telefono": telefono_limpio[:20],  # Truncar para respetar el límite de la columna
            "direccion": direccion_limpia,
        })

        # Insertar por bloques y limpiar memoria RAM de inmediato
        if (i + 1) % BATCH_SIZE == 0:
            session.bulk_insert_mappings(Personas_Juan, registros)
            session.commit()
            registros.clear()
            print(f"Insertados {i + 1} registros...")

    # Insertar el último lote si quedaron registros remanentes
    if registros:
        session.bulk_insert_mappings(Personas_Juan, registros)
        session.commit()

    print("Inserción completa: 100,000 registros guardados.")

    # Verificar conteo final
    total = session.query(Personas_Juan).count()
    print(f"Total de registros en la tabla: {total}")

    session.close()

if __name__ == "__main__":
    main()
