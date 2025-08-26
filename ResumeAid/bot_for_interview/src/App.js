import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useReactMediaRecorder } from 'react-media-recorder';
import './App.css';

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescriptionFile, setJobDescriptionFile] = useState(null);
  const [interviewStarted, setInterviewStarted] = useState(false);
  const [audioSrc, setAudioSrc] = useState(null);
  const [interviewFinished, setInterviewFinished] = useState(false);

  const handleResumeFileChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleJobDescriptionFileChange = (e) => {
    setJobDescriptionFile(e.target.files[0]);
  };

  const handleInterviewStart = (audioUrl) => {
    setInterviewStarted(true);
    setAudioSrc(audioUrl);
  };

  const submitAudioResponse = async (blob) => {
    const formData = new FormData();
    formData.append('audio', blob, 'response.webm');
  
    try {
      const response = await axios.post('http://localhost:8000/submit_response', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob',
      });
  
      const audioUrl = URL.createObjectURL(response.data);
      setAudioSrc(audioUrl);
  
      if (response.headers['content-type'] === 'audio/webm' && response.data.size === 0) {
        setInterviewFinished(true);
      }
    } catch (error) {
      console.error('Error during audio response submission:', error);
      alert('Failed to submit audio response');
    }
  };

  const startInterview = async () => {
    try {
      const response = await axios.post('http://localhost:8000/interview', {}, {
        responseType: 'blob',
      });
      const audioUrl = URL.createObjectURL(response.data);
      handleInterviewStart(audioUrl);
    } catch (error) {
      console.error('Error during interview:', error);
      alert('Failed to start interview');
    }
  };

  return (
    <div className="App">
      <h1>Interview Bot</h1>
      <FileUpload 
        onResumeFileChange={handleResumeFileChange} 
        onJobDescriptionFileChange={handleJobDescriptionFileChange} 
      />
      <InterviewControl
        resumeFile={resumeFile}
        jobDescriptionFile={jobDescriptionFile}
        onInterviewStart={handleInterviewStart}
        startInterview={startInterview}
        interviewStarted={interviewStarted}
        submitAudioResponse={submitAudioResponse}
        interviewFinished={interviewFinished}
      />
      {audioSrc && <AudioPlayer src={audioSrc} />}
    </div>
  );
}

function FileUpload({ onResumeFileChange, onJobDescriptionFileChange }) {
  return (
    <div className="file-upload">
      <div>
        <label>Upload Resume:</label>
        <input type="file" onChange={onResumeFileChange} />
      </div>
      <div>
        <label>Upload Job Description:</label>
        <input type="file" onChange={onJobDescriptionFileChange} />
      </div>
    </div>
  );
}
function InterviewControl({ resumeFile, jobDescriptionFile, onInterviewStart, startInterview, interviewStarted, submitAudioResponse, interviewFinished }) {
  const {
    status,
    startRecording,
    stopRecording,
    mediaBlobUrl,
    clearBlobUrl,
  } = useReactMediaRecorder({
    audio: true,
    clearRecordedBlobs: true,
    mediaRecorderOptions: {
      mimeType: 'audio/webm',
    },
  });

  // Debugging information for MediaRecorder
  useEffect(() => {
    console.log('MediaRecorder Hook Initialized');
    console.log('Status:', status);
    console.log('Media Blob URL:', mediaBlobUrl);
    
    return () => {
      console.log('Cleanup - clearing mediaBlobUrl');
      clearBlobUrl();
    };
  }, [status, mediaBlobUrl, clearBlobUrl]);

  const uploadResume = async () => {
    console.log('Uploading Resume...');
    const formData = new FormData();
    formData.append('resume', resumeFile);

    try {
      await axios.post('http://localhost:8000/upload_resume', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('Resume uploaded successfully!');
    } catch (error) {
      console.error('Error uploading resume:', error);
      alert('Failed to upload resume');
    }
  };

  const uploadJobDescription = async () => {
    console.log('Uploading Job Description...');
    const formData = new FormData();
    formData.append('job_description', jobDescriptionFile);

    try {
      await axios.post('http://localhost:8000/upload_job_description', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('Job description uploaded successfully!');
    } catch (error) {
      console.error('Error uploading job description:', error);
      alert('Failed to upload job description');
    }
  };

  const stopAndSubmitRecording = async () => {
    console.log('Stopping Recording...');
    stopRecording();
    if (mediaBlobUrl) {
      const blob = await fetch(mediaBlobUrl).then((res) => res.blob());
      const audioBlob = new Blob([blob], { type: 'audio/webm' });
      console.log('Submitting Audio Response...');
      await submitAudioResponse(audioBlob);
      clearBlobUrl();
      startInterview();
    }
  };

  return (
    <div className="interview-control">
      <button onClick={uploadResume} disabled={!resumeFile}>
        Upload Resume
      </button>
      <button onClick={uploadJobDescription} disabled={!jobDescriptionFile}>
        Upload Job Description
      </button>
      {!interviewStarted && (
        <button onClick={startInterview} disabled={!resumeFile || !jobDescriptionFile}>
          Start Interview
        </button>
      )}
      {interviewStarted && !interviewFinished && (
        <div className="response-section">
          {status === 'idle' && (
            <button onClick={startRecording}>Start Recording</button>
          )}
          {status === 'recording' && (
            <button onClick={stopAndSubmitRecording}>Stop & Submit Recording</button>
          )}
          {status === 'stopped' && mediaBlobUrl && (
            <audio src={mediaBlobUrl} controls autoPlay />
          )}
        </div>
      )}
      {interviewFinished && <p>Thank you for completing the interview!</p>}
    </div>
  );
}