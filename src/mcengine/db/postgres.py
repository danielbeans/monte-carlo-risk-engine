"""
! TODO:
    - Use ORM
    - Decouple methods from commission simulation logic
"""
from __future__ import annotations

from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor

from mcengine.config import settings


class PostgresService:
    def __init__(self) -> None:
        pass

    def _get_connection(self) -> psycopg2.extensions.connection:
        """Create a new database connection."""
        return psycopg2.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            user=settings.postgres_user,
            password=settings.postgres_password,
            database=settings.postgres_db,
        )

    def initialize_schema(self) -> None:
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS commission_simulation_results (
                        job_id VARCHAR(255) PRIMARY KEY,
                        result_json JSONB NOT NULL,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                    );
                    
                    CREATE INDEX IF NOT EXISTS idx_commission_results_created_at 
                    ON commission_simulation_results(created_at);
                    """
                )
                conn.commit()
        finally:
            conn.close()

    def save_result(self, job_id: str, result_json: str) -> None:
        conn = self._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO commission_simulation_results (job_id, result_json, updated_at)
                    VALUES (%s, %s, NOW())
                    ON CONFLICT (job_id) 
                    DO UPDATE SET 
                        result_json = EXCLUDED.result_json,
                        updated_at = NOW()
                    """,
                    (job_id, result_json),
                )
                conn.commit()
        finally:
            conn.close()

    def get_result(self, job_id: str) -> dict[str, Any] | None:
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT result_json 
                    FROM commission_simulation_results 
                    WHERE job_id = %s
                    """,
                    (job_id,),
                )
                row = cur.fetchone()
                if row is None:
                    return None
                return row["result_json"]
        finally:
            conn.close()

    def close(self) -> None:
        pass


POSTGRES_SERVICE = PostgresService()


def get_postgres_service() -> PostgresService:
    return POSTGRES_SERVICE

