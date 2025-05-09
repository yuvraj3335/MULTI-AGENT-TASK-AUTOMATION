import whisper
import asyncio
import logging

logger = logging.getLogger(__name__)

class AudioToTextAgent:
    async def transcribe(self, file_path, retries=3):
        whisper_model = whisper.load_model("base")
        for attempt in range(retries):
            try:
                logger.info(f"Attempting transcription for {file_path}, attempt {attempt + 1}")
                result = whisper_model.transcribe(file_path)
                logger.info(f"Transcription successful for {file_path}")
                return result["text"]
            except Exception as e:
                logger.error(f"Transcription attempt {attempt + 1} failed for {file_path}: {e}")
                if attempt == retries - 1:
                    raise Exception("Transcription failed after retries")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff