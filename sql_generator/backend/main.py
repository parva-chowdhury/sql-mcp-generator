from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import SQLAgent
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = SQLAgent()

class QueryRequest(BaseModel):
    query: str
    history: list = []

class FeedbackRequest(BaseModel):
    query: str
    sql: str
    rating: str  # "Good" or "Bad"

class ExecuteRequest(BaseModel):
    sql: str

@app.post("/api/generate_sql")
async def generate_sql(request: QueryRequest):
    try:
        sql = await agent.generate_sql(request.query, request.history)
        return {"sql": sql}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/execute_sql")
async def execute_sql(request: ExecuteRequest):
    try:
        result = agent.execute_sql(request.sql)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/feedback")
async def save_feedback(request: FeedbackRequest):
    try:
        agent.save_feedback(request.query, request.sql, request.rating)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
