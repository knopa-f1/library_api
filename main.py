import uvicorn
from fastapi import FastAPI

import app.api.endpoints as endpoints

app = FastAPI(title="Library API")

app.include_router(endpoints.authors_router)
app.include_router(endpoints.books_router)
app.include_router(endpoints.borrows_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app")
