from fastapi import FastAPI
from routes import user_routes, device_routes, device_log_routes

app = FastAPI(title="IOTConnect Clone", version="1.0.0")

# INCLUDNG ROUTES
app.include_router(user_routes.router, prefix="/api/users", tags=["users"])
app.include_router(device_routes.router, prefix="/api/devices", tags=["devices"])
app.include_router(device_log_routes.router, prefix="/api/device-logs", tags=["device-logs"])

@app.get("/")
def read_root():
    return {"message": "IOTConnect Clone API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)