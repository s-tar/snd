from base.app import app
import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        root_path="/api",
        port=5000,
        reload=True,
    )
