let mediaRecorder;
let audioChunks = [];

document.getElementById("start").addEventListener("click", async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        const formData = new FormData();
        formData.append("audio_file", audioBlob, "user_audio.wav");

        const response = await fetch("http://127.0.0.1:8000/ai_teacher/", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();
        document.getElementById("feedback").innerHTML = `
            <p><strong>Transcription:</strong> ${data.transcription}</p>
            <p><strong>Feedback:</strong> ${data.feedback}</p>
        `;
        document.getElementById("audioPlayer").src = data.audio_file;
    };

    document.getElementById("start").disabled = true;
    document.getElementById("stop").disabled = false;
});

document.getElementById("stop").addEventListener("click", () => {
    mediaRecorder.stop();
    document.getElementById("start").disabled = false;
    document.getElementById("stop").disabled = true;
});
