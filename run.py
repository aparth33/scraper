import os
import uvicorn
from dotenv import load_dotenv

load_dotenv('.env')

port = os.getenv('PORT')

# Ensure the port is an integer
if port is not None:
    port = int(port)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=os.getenv('LOCALHOST_URL'), port=port, reload=True)
