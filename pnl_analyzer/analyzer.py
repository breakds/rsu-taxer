import os

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pnl_analyzer.protocols import PlotResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_PATH = Path(
    os.getenv(
        "PNL_FRONTEND",
        str(Path(__file__).parent.parent / "webapp" / "dist"),
    )
)
app.mount("/assets", StaticFiles(directory=FRONTEND_PATH / "assets", html=True))


@app.get("/")
async def serve_ui():
    return FileResponse(FRONTEND_PATH / "index.html")


@app.get(
    "/pnl",
    response_model=PlotResponse,
    response_model_by_alias=True,
)
async def pnl(
    longterm: str = Query(..., description="Amount of long-term capital gain in $"),
    shorterm: str = Query(..., description="Amount of short-term capital gain in $"),
    settlement: str = Query(..., description="The settlement price in $"),
    shares: str = Query(..., description="The number of shares"),
) -> PlotResponse:
    return PlotResponse()


def main():
    port = int(os.getenv("PNL_SERVER_PORT", "31415"))
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
