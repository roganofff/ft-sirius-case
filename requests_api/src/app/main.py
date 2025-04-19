# from contextlib import asynccontextmanager
# from fastapi import FastAPI
# from app.db.connection import get_clickhouse_client, close_clickhouse
# from app.routes import requests
# from app.config import settings
# from app.utils.logger import logger

# # @asynccontextmanager
# # async def lifespan(app: FastAPI):
# #     try:
# #         async with get_clickhouse_client() as client:
# #             await client.execute("SELECT 1")
# #             logger.info("Database connection verified")
# #     except Exception as e:
# #         logger.critical(f"Database connection failed: {str(e)}")
# #         raise
    
# #     yield
    
# #     await close_clickhouse()
# #     logger.info("Application shutdown complete")

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     client = await get_clickhouse_client()
#     yield {"clickhouse": client}
#     await close_clickhouse(client)

# app = FastAPI(
#     title="Sirius FT Requests API",
#     lifespan=lifespan,
#     docs_url="/api/docs",
#     redoc_url="/api/redoc"
# )

# app.include_router(requests.router)

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy"}


from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.connection import clickhouse_client
from app.routes import requests, similarity
from app.config import settings
from app.utils.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with clickhouse_client() as client:
        yield {"client": client}

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
app.include_router(requests.router)
app.include_router(similarity.router)