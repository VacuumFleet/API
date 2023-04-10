import uvicorn
import os

if __name__ == "__main__":
    uvicorn.run(
        "server.app:app", host="0.0.0.0", port=os.environ.get("PORT", 8000), reload=True
    )
