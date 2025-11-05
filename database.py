from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
import pymysql
import os

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency for getting DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def execute_sql_file(filepath: str, connection):
    """Execute a SQL file"""
    print(f"Executing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as file:
        sql_content = file.read()
        
        # Split by delimiter blocks
        if 'DELIMITER' in sql_content:
            # Handle files with DELIMITER (triggers, procedures)
            statements = []
            current_delimiter = ';'
            temp_statement = ''
            
            for line in sql_content.split('\n'):
                if line.strip().startswith('DELIMITER'):
                    if temp_statement.strip():
                        statements.append(temp_statement.strip())
                        temp_statement = ''
                    current_delimiter = line.strip().split()[-1]
                    continue
                
                temp_statement += line + '\n'
                
                if current_delimiter in line:
                    statements.append(temp_statement.strip().rstrip(current_delimiter))
                    temp_statement = ''
            
            if temp_statement.strip():
                statements.append(temp_statement.strip())
            
            for statement in statements:
                if statement and not statement.startswith('--'):
                    try:
                        connection.execute(text(statement))
                    except Exception as e:
                        print(f"Warning in statement: {e}")
        else:
            # Handle regular SQL files
            statements = sql_content.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    try:
                        connection.execute(text(statement))
                    except Exception as e:
                        print(f"Warning: {e}")
        
        connection.commit()
        print(f"✓ {filepath} executed successfully")


def setup_database():
    """Setup database from SQL files"""
    sql_dir = settings.SQL_FILES_DIR
    
    # Order matters! Updated for your folder structure
    sql_files = [
        'schemas/database.sql',
        'schemas/tables.sql',
        'schemas/views.sql',
        'procedure/procedures.sql',
        'triggers/triggers.sql',
        'sample_data/sample_data.sql'
    ]
    
    # First connect without database to create it
    initial_url = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}"
    initial_engine = create_engine(initial_url)
    
    try:
        with initial_engine.connect() as conn:
            # Execute database.sql to create database
            db_file = os.path.join(sql_dir, 'schemas/database.sql')
            if os.path.exists(db_file):
                execute_sql_file(db_file, conn)
        
        initial_engine.dispose()
        
        # Now connect to the actual database and run remaining files
        with engine.connect() as conn:
            for sql_file in sql_files[1:]:  # Skip database.sql
                filepath = os.path.join(sql_dir, sql_file)
                if os.path.exists(filepath):
                    execute_sql_file(filepath, conn)
                else:
                    print(f"⚠️ Warning: {sql_file} not found at {filepath}, skipping...")
        
        print("\n✅ Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error setting up database: {e}")
        import traceback
        traceback.print_exc()
        return False