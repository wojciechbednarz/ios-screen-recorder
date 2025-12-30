import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from './api';
import type { Recording } from './api';
import { Button, Card, CardHeader, CardContent, CardTitle, CardDescription, Badge, RecordingCard } from './components';

function App() {
  const queryClient = useQueryClient();
  const [isRecording, setIsRecording] = useState(false);
  const [currentFile, setCurrentFile] = useState<string | null>(null);
  const [recordingDuration, setRecordingDuration] = useState(0);

  // Timer for recording duration
  useEffect(() => {
    let interval: number | undefined;
    if (isRecording) {
      interval = window.setInterval(() => {
        setRecordingDuration(prev => prev + 1);
      }, 1000);
    } else {
      setRecordingDuration(0);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isRecording]);

  const { data: recordings, isLoading } = useQuery({
    queryKey: ['recordings'],
    queryFn: api.listRecordings,
    refetchInterval: 5000,
  });

  const startMutation = useMutation({
    mutationFn: api.startRecording,
    onSuccess: (data) => {
      console.log('Start recording success:', data);
      setIsRecording(true);
      setCurrentFile(data.filename || null);
    },
    onError: (error) => {
      console.error('Start recording error:', error);
      alert('Failed to start recording: ' + error);
    }
  });

  const stopMutation = useMutation({
    mutationFn: api.stopRecording,
    onSuccess: () => {
      console.log('Stop recording success');
      setIsRecording(false);
      setCurrentFile(null);
      queryClient.invalidateQueries({ queryKey: ['recordings'] });
    },
    onError: (error) => {
      console.error('Stop recording error:', error);
      alert('Failed to stop recording: ' + error);
    }
  });

  const handleToggle = () => {
    console.log('Toggling recording. Current state:', isRecording);
    if (isRecording) {
      stopMutation.mutate();
    } else {
      startMutation.mutate();
    }
  };

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const formatFileSize = (bytes: number) => {
    return (bytes / 1024 / 1024).toFixed(2);
  };

  const totalSize = recordings?.reduce((acc, rec) => acc + rec.size_bytes, 0) || 0;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center shadow-sm">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Appium Screen Recorder</h1>
                <p className="text-sm text-gray-500">Manage your iOS screen recordings</p>
              </div>
            </div>

            {/* Stats */}
            <div className="flex gap-4">
              <div className="text-center px-6 py-3 bg-gray-50 rounded-lg border border-gray-200">
                <div className="text-xs font-medium text-gray-500 uppercase tracking-wide">Total Files</div>
                <div className="text-2xl font-bold text-gray-900 mt-1">{recordings?.length || 0}</div>
              </div>
              <div className="text-center px-6 py-3 bg-gray-50 rounded-lg border border-gray-200">
                <div className="text-xs font-medium text-gray-500 uppercase tracking-wide">Total Size</div>
                <div className="text-2xl font-bold text-gray-900 mt-1">{formatFileSize(totalSize)} MB</div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Recording Control Card */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <CardTitle>Recording Control</CardTitle>
                <CardDescription>Start or stop your screen recording session</CardDescription>

                {/* Recording Status */}
                {isRecording && (
                  <div className="mt-4 flex items-center gap-3 bg-red-50 border border-red-200 rounded-lg px-4 py-3">
                    <div className="relative flex items-center justify-center">
                      <div className="w-2.5 h-2.5 bg-red-500 rounded-full animate-pulse"></div>
                      <div className="absolute w-2.5 h-2.5 bg-red-500 rounded-full animate-ping"></div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-semibold text-red-900">Recording in Progress</div>
                      <div className="text-xs text-red-600 truncate">{currentFile}</div>
                    </div>
                    <Badge variant="error" className="text-base font-mono font-bold px-3 py-1">
                      {formatDuration(recordingDuration)}
                    </Badge>
                  </div>
                )}
              </div>

              <Button
                onClick={handleToggle}
                variant={isRecording ? 'destructive' : 'primary'}
                size="lg"
                isLoading={startMutation.isPending || stopMutation.isPending}
                className="ml-6"
              >
                {isRecording ? (
                  <>
                    <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                      <rect x="6" y="6" width="12" height="12" rx="2" />
                    </svg>
                    Stop Recording
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                      <circle cx="12" cy="12" r="4" />
                    </svg>
                    Start Recording
                  </>
                )}
              </Button>
            </div>
          </CardHeader>
        </Card>

        {/* Recordings List Card */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Recent Recordings</CardTitle>
              <Badge variant="default">{recordings?.length || 0} files</Badge>
            </div>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="flex flex-col items-center justify-center py-16">
                <svg className="animate-spin h-6 w-6 text-blue-600 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="5" stroke="currentColor" strokeWidth="3"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <p className="text-sm text-gray-500">Loading recordings...</p>
              </div>
            ) : recordings?.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-8 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
                <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center mb-3">
                  <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                </div>
                <h3 className="text-base font-semibold text-gray-900 mb-1">No recordings yet</h3>
                <p className="text-sm text-gray-500">Click "Start Recording" to create your first recording</p>
              </div>
            ) : (
              <div className="space-y-3">
                {recordings?.map((rec: Recording) => (
                  <RecordingCard key={rec.filename} recording={rec} />
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </main>
    </div>
  );
}

export default App;
