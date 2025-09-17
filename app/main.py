from fastapi import FastAPI

app = FastAPI(
    title="Coinsec API", description="基于 AI 技术的智能记账系统 API", version="0.1.0"
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Coinsec API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
