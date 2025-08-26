import React, { useState, useEffect } from 'react';
import axios from 'axios';



function App() {
    const [pdfFile, setPdfFile] = useState(null);
    const [audioFile, setAudioFile] = useState(null);
    const [questions, setQuestions] = useState([]);
    const [audioResponse, setAudioResponse] = useState([]);

    const handlePdfUpload = (event) => {
        setPdfFile(event.target.files[0]);
    };

    const handleAudioUpload = (event) => {
        setAudioFile(event.target.files[0]);
    };

    const generateQuestions = async () => {
        if (!pdfFile) {
            alert("Please upload a PDF file first.");
            return;
        }
        const formData = new FormData();
        formData.append('resume', pdfFile);
        // alert("Created form");
        try {
            const response = await axios.post('http://localhost:3000/upload_resume', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            if (response.data.questions) {
                console.log('Received questions:', response.data.questions);
                setQuestions(response.data.questions);
            } else {
                console.error('Error:', response.data.error);
            }
        } catch (error) {
            console.error('Error generating questions:', error);
        }
    };

    const generateAudioResponse = async () => {
        if (!audioFile) {
            alert("Please upload an audio file first.");
            return;
        }
        const formData = new FormData();
        formData.append('audio', audioFile);

        try {
            const response = await axios.post('http://localhost:3000/listen_audio', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                // responseType: 'blob', // Important for handling audio response
            });
            if (response.data.transcription) {
              //console.log('Received questions:', response.data.questions);
              setAudioResponse(response.data.transcription);
            } else {
                console.error('Error:', response.data.error);
            }
            // console.log("Response " + response.data.transcription);
            // setAudioResponse(URL.createObjectURL(response.data));
        } catch (error) {
            console.error('Error generating audio response:', error);
        }
    };

      return (
        <div className="App">
            <h1>Interview Helper</h1>
            <div>
                <h2>Upload Resume PDF</h2>
                <input type="file" accept=".pdf" onChange={handlePdfUpload} />
                <button onClick={generateQuestions}>Generate Questions</button>
            </div>
            <div>
                <h2>Generated Questions</h2>
                <ul>
                    {questions.map((question, index) => (
                        <li key={index}>{question}</li>
                    ))}
                </ul>
            </div>
            <div>
                <h2>Upload Audio File</h2>
                <input type="file" accept="audio/mp3" onChange={handleAudioUpload} />
                <button onClick={generateAudioResponse}>Get Audio Response</button>
            </div>
            <div>
                <h2>Audio Response</h2>
                {/* {audioResponse && (
                    <audio controls src={audioResponse}>
                        Your browser does not support the audio element.
                    </audio>
                )} */}
                <ul>
                    {audioResponse.map((question, index) => (
                        <li key={index}>{question}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default App;
