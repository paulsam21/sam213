from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

def fetch_transcript(video_url):
    try:
        
        if "watch?v=" in video_url:
            video_id = video_url.split("watch?v=")[-1]
        elif "youtu.be/" in video_url:
            video_id = video_url.split("youtu.be/")[-1]
        else:
            return None

        
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        
        full_text = " ".join([t['text'] for t in transcript])
        return full_text
    except Exception as e:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    error = None
    if request.method == "POST":
        video_url = request.form.get("video_url")
        if video_url:
            transcript = fetch_transcript(video_url)
            if transcript:
                summary = transcript[:5000] 
            else:
                error = "Transcript not available for this video."
    return render_template("index.html", summary=summary, error=error)

if __name__ == "__main__":
    app.run(debug=True)
