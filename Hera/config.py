class Config:
    # Configuración base
    DEBUG = True
    TESTING = True
    
    # Configuración de Base de Datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Tu configuración de base de datos
    # NOTA: Es necesario que configures esto para el funcionamiento de la aplicación
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://#user:password:@host:/name' 

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True