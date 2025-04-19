from fastapi import APIRouter, HTTPException, status
from app.db.connection import clickhouse_client
from app.models.schemas import RequestCreate, RequestOut
from app.utils.logger import logger

router = APIRouter(
    prefix="/api/requests",
    tags=["Requests"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error"
        }
    }
)

@router.post("", response_model=RequestOut, status_code=201)
async def create_request(request: RequestCreate):
    try:
        async with clickhouse_client() as client:
            query = """
                INSERT INTO requests (
                    user_id,
                    description
                ) VALUES
            """
            values = [
                (request.user_id, request.description)
            ]
            await client.execute(query, *values)

            result = await client.fetchrow("""
                SELECT 
                    id::String as id,
                    user_id,
                    description,
                    created_at,
                    updated_at
                FROM requests
                ORDER BY created_at DESC
                LIMIT 1
            """)

            logger.info(f"Created request ID: {result['id']}")
            return result

    except Exception as e:
        logger.error(f"Request creation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )



@router.get("", response_model=list[RequestOut])
async def get_all_requests():
    async with clickhouse_client() as client:
        result = await client.fetch("""
            SELECT 
                id::String as id,
                user_id,
                description,  # Убрали title
                created_at,
                updated_at
            FROM requests
            ORDER BY created_at DESC
        """)
        return result