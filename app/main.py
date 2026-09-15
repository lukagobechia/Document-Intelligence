import logging

from fastapi import FastAPI, UploadFile, File, HTTPException

from app.document import extract_text
from app.foundry import analyze_document
from app.logging_config import setup_logging


setup_logging()

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md",
}


app = FastAPI(
    title="Microsoft Foundry Document Intelligence API",
    description="AI-powered document analysis API using Microsoft Foundry.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Document Intelligence API is running"
    }


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    filename = file.filename or ""

    logger.info(
        "Document analysis requested: filename=%s",
        filename,
    )

    try:
        extension = "." + filename.split(".")[-1].lower() if "." in filename else ""

        if extension not in ALLOWED_EXTENSIONS:
            logger.warning(
                "Unsupported file type: filename=%s",
                filename,
            )

            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Use PDF, TXT, or Markdown.",
            )

        content = await file.read()

        if len(content) > MAX_FILE_SIZE:
            logger.warning(
                "File too large: filename=%s size=%d",
                filename,
                len(content),
            )

            raise HTTPException(
                status_code=413,
                detail="The uploaded file is too large. Maximum size is 10 MB.",
            )

        if not content:
            logger.warning(
                "Empty document received: filename=%s",
                filename,
            )

            raise HTTPException(
                status_code=400,
                detail="The uploaded document is empty.",
            )

        text = extract_text(
            filename=filename,
            content=content,
        )

        if not text.strip():
            logger.warning(
                "No text extracted: filename=%s",
                filename,
            )

            raise HTTPException(
                status_code=400,
                detail="No readable text was found in the document.",
            )

        logger.info(
            "Document text extracted successfully: filename=%s",
            filename,
        )

        result = analyze_document(text)

        logger.info(
            "Document analysis completed: filename=%s",
            filename,
        )

        return {
            "filename": filename,
            "analysis": result,
        }

    except HTTPException:
        raise

    except ValueError as error:
        logger.warning(
            "Invalid document: filename=%s error=%s",
            filename,
            error,
        )

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception:
        logger.exception(
            "Unexpected error during document analysis: filename=%s",
            filename,
        )

        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while analyzing the document.",
        )