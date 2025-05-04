from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.messages import router
from app.domain.model.errors import MessageNotFoundError, ValidationError

app = FastAPI(
    title="Palindrome Checker API",
    description="REST API to check if a message is a palindrome",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.exception_handler(MessageNotFoundError)
async def message_not_found_handler(request: Request, exc: MessageNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc) or "Message not found"},
    )


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc) or "Validation error"},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500, content={"detail": "An unexpected error occurred."}
    )
