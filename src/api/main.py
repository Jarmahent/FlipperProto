from fastapi import FastAPI
from api.vehicles import router as vehicles_router
from api.parts import router as parts_router
import uvicorn
from api.metadata import metadata_tag_info



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

    return app



if __name__ == "__main__":
    uvicorn.run("main:init_app", host="0.0.0.0", port=8080, factory=True)
