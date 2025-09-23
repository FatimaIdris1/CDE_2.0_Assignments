import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import logging
import sys
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
try:
    load_dotenv("config.env")
except Exception as e:
    logger.warning(f"Could not load config.env: {e}")

def validate_environment() -> bool:
    """Validate that all required environment variables are set."""
    required_vars = ["DATA_URL", "POSTGRES_USER", "POSTGRES_PASSWORD", 
                    "POSTGRES_DB", "POSTGRES_HOST", "POSTGRES_PORT"]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        return False
    return True

# Load environment variables
data_url = os.getenv("DATA_URL")
pg_user = os.getenv("POSTGRES_USER")
pg_password = os.getenv("POSTGRES_PASSWORD")
pg_db = os.getenv("POSTGRES_DB")
pg_host = os.getenv("POSTGRES_HOST")
pg_port = os.getenv("POSTGRES_PORT")


def extract(data_url: str) -> Optional[pd.DataFrame]:
    """Extract data from a CSV URL into a DataFrame."""
    try:
        df = pd.read_csv(data_url)
        logger.info(f"Extracted {len(df)} rows from {data_url}")
        return df
    except Exception as e:
        logger.error(f"Failed to extract data from {data_url}: {e}")
        return None

def transform(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """Clean and prepare the data with more careful handling."""
    try:
        initial_rows = len(df)
        
        # Drop rows only if ALL values are null
        df = df.dropna(how='all')

        
        # Column name transformation
        df.columns = [
            col.strip().lower()
            .replace(" ", "_")
            .replace("-", "_")
            .replace(".", "_")
            for col in df.columns
        ]
        
        # Ensure column names start with letter or underscore
        df.columns = [
            f"col_{col}" if col[0].isdigit() else col 
            for col in df.columns
        ]
        
        logger.info(f"Transformed data: {initial_rows} -> {len(df)} rows")
        return df
        
    except Exception as e:
        logger.error(f"Failed to transform data: {e}")
        return None

def load(df: pd.DataFrame, table_name: str = "etl_table", if_exists: str = "replace") -> bool:
    """Load DataFrame into PostgreSQL table with proper connection handling."""
    engine = None
    try:
        connection_string = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"

        engine = create_engine(connection_string, pool_pre_ping=True)
        
        df.to_sql(table_name, engine, if_exists=if_exists, index=False, method='multi')
        logger.info(f"Loaded {len(df)} rows into table '{table_name}'")
        return True
        
    except Exception as e:
        logger.error(f"Failed to load data into {table_name}: {e}")
        return False
    finally:
        if engine:
            engine.dispose()

def etl_pipeline() -> bool:
    """Run the full ETL process with comprehensive error handling."""
    try:
        # Validate environment
        if not validate_environment():
            return False
        
        # Extract
        df = extract(data_url)
        if df is None or df.empty:
            logger.error("No data extracted, stopping pipeline")
            return False
        
        # Transform
        df_transformed = transform(df)
        if df_transformed is None or df_transformed.empty:
            logger.error("No data after transformation, stopping pipeline")
            return False
        
        # Load
        success = load(df_transformed, table_name="etl_results")
        if not success:
            logger.error("Failed to load data, pipeline failed")
            return False
        
        logger.info("ETL pipeline completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"ETL pipeline failed with unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = etl_pipeline()
    sys.exit(0 if success else 1)