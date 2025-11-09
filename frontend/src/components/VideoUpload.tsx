import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

interface VideoUploadProps {
  onVideoUpload: (file: File) => void;
  isAnalyzing?: boolean;
}

const VideoUpload: React.FC<VideoUploadProps> = ({ onVideoUpload, isAnalyzing = false }) => {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setUploadedFile(file);
      onVideoUpload(file);
    }
  }, [onVideoUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'video/mp4': ['.mp4'],
      'video/avi': ['.avi'],
      'video/mov': ['.mov']
    },
    maxFiles: 1,
    disabled: isAnalyzing
  });

  return (
    <div className="card">
      <h3 className="text-xl font-semibold mb-4 text-gray-800">📹 Upload Fish Pond Video</h3>
      
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all duration-200
          ${isDragActive 
            ? 'border-primary-500 bg-primary-50' 
            : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
          }
          ${isAnalyzing ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        {isAnalyzing ? (
          <div className="flex flex-col items-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mb-4"></div>
            <p className="text-lg font-medium text-gray-600">Analyzing video...</p>
            <p className="text-sm text-gray-500">This may take a few moments</p>
          </div>
        ) : uploadedFile ? (
          <div className="flex flex-col items-center">
            <div className="text-4xl mb-4">✅</div>
            <p className="text-lg font-medium text-gray-700">{uploadedFile.name}</p>
            <p className="text-sm text-gray-500">
              {(uploadedFile.size / (1024 * 1024)).toFixed(2)} MB
            </p>
            <p className="text-sm text-primary-600 mt-2">Click to replace or drag another video</p>
          </div>
        ) : (
          <div className="flex flex-col items-center">
            <div className="text-4xl mb-4">🎥</div>
            <p className="text-lg font-medium text-gray-700">
              {isDragActive ? 'Drop the video here' : 'Drag & drop a video here'}
            </p>
            <p className="text-sm text-gray-500 mt-2">or click to select a file</p>
            <p className="text-xs text-gray-400 mt-4">
              Supported formats: MP4, AVI, MOV (Max: 100MB)
            </p>
          </div>
        )}
      </div>

      {/* Demo Video Option */}
      <div className="mt-4 p-4 bg-aqua-50 rounded-lg border border-aqua-200">
        <h4 className="font-medium text-aqua-800 mb-2">🎬 Try Demo Video</h4>
        <p className="text-sm text-aqua-600 mb-3">
          No video? Use our sample fish pond footage for testing
        </p>
        <button
          onClick={() => {
            // Simulate demo video upload
            const demoFile = new File(['demo'], 'demo_fish_pond.mp4', { type: 'video/mp4' });
            setUploadedFile(demoFile);
            onVideoUpload(demoFile);
          }}
          className="btn-secondary text-sm"
          disabled={isAnalyzing}
        >
          Load Demo Video
        </button>
      </div>
    </div>
  );
};

export default VideoUpload;