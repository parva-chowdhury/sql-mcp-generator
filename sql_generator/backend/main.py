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

@app.post("/api/generate_sql")
async def generate_sql(request: QueryRequest):
    try:
        sql = await agent.generate_sql(request.query)
        return {"sql": sql}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
