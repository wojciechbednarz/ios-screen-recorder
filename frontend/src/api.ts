import axios from 'axios';

// Use environment variable for API URL or default to empty string (relative) for production
const API_URL = import.meta.env.VITE_API_URL || '';

export interface RecordingStatus {
    is_recording: boolean;
    filename?: string;
}

export interface Recording {
    filename: string;
    size_bytes: number;
    created_at: string;
    download_url: string;
}

export const api = {
    startRecording: async () => {
        const response = await axios.post<RecordingStatus>(`${API_URL}/recording/start`, {
            filename_prefix: 'recording'
        });
        return response.data;
    },
    stopRecording: async () => {
        const response = await axios.post<Recording>(`${API_URL}/recording/stop`);
        return {
            ...response.data,
            download_url: `${API_URL}${response.data.download_url}`
        };
    },
    listRecordings: async () => {
        const response = await axios.get<Recording[]>(`${API_URL}/recordings`);
        return response.data.map(rec => ({
            ...rec,
            download_url: `${API_URL}${rec.download_url}`
        }));
    },
    getDownloadUrl: (filename: string) => `${API_URL}/recordings/${filename}`
};
