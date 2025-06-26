from fastapi import FastAPI
from api.vehicles import router as vehicles_router
from api.parts import router as parts_router
from api.listings import router as listings_router
import uvicorn
from api.metadata import metadata_tag_info
from fastapi.middleware.cors import CORSMiddleware



def init_app():
    app = FastAPI(
        title="Flipper API",
        version="0.0.1",
        openapi_tags=metadata_tag_info,
        # lifespan=lifespan,
        openapi_url="/flipper/openapi.json",
        docs_url="/flipper/swagger",
        redoc_url="/flipper/redoc",
        swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
    )


    app.include_router(vehicles_router)
    app.include_router(parts_router)
    app.include_router(listings_router)

    # Enable CORS for all origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app



if __name__ == "__main__":
    uvicorn.run("main:init_app", host="0.0.0.0", port=8080, factory=True)
