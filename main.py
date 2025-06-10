from fastapi import FastAPI
from fastapi.responses import JSONResponse
from urllib.parse import parse_qs, urlparse
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()

@app.get("/transcript")
def get_transcript(video_url: str):
    """Return the transcript for a given YouTube video URL."""
    try:
        # Extract the video id reliably even if additional query
        # parameters are present in the URL.
        parsed_url = urlparse(video_url)
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get("v", [parsed_url.path.split("/")[-1]])[0]

        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return {"transcript": transcript}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
