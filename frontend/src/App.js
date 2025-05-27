import React, { useState } from 'react';
import { 
  Container, 
  Box, 
  Typography, 
  TextField, 
  Button, 
  Paper,
  CircularProgress,
  Alert
} from '@mui/material';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

function App() {
  const [token, setToken] = useState('');
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onDrop = (acceptedFiles) => {
    setFile(acceptedFiles[0]);
    setError(null);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif']
    },
    multiple: false
  });

  const handleModerate = async () => {
    if (!token) {
      setError('Please enter a token');
      return;
    }
    if (!file) {
      setError('Please select an image');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/moderate`,
        formData,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          Image Moderation API
        </Typography>

        <Paper sx={{ p: 3, mb: 3 }}>
          <TextField
            fullWidth
            label="API Token"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            margin="normal"
          />
        </Paper>

        <Paper sx={{ p: 3, mb: 3 }}>
          <Box
            {...getRootProps()}
            sx={{
              border: '2px dashed #ccc',
              borderRadius: 2,
              p: 3,
              textAlign: 'center',
              cursor: 'pointer',
              bgcolor: isDragActive ? '#f0f0f0' : 'white'
            }}
          >
            <input {...getInputProps()} />
            {file ? (
              <Typography>{file.name}</Typography>
            ) : (
              <Typography>
                {isDragActive
                  ? 'Drop the image here'
                  : 'Drag and drop an image, or click to select'}
              </Typography>
            )}
          </Box>
        </Paper>

        <Box sx={{ display: 'flex', justifyContent: 'center', mb: 3 }}>
          <Button
            variant="contained"
            onClick={handleModerate}
            disabled={loading || !file || !token}
          >
            {loading ? <CircularProgress size={24} /> : 'Moderate Image'}
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {result && (
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Moderation Results
            </Typography>
            <Typography>
              Overall Status: {result.safe ? 'Safe' : 'Unsafe'}
            </Typography>
            <Typography variant="subtitle1" sx={{ mt: 2 }}>
              Categories:
            </Typography>
            {Object.entries(result.categories).map(([category, score]) => (
              <Typography key={category}>
                {category}: {(score * 100).toFixed(1)}%
              </Typography>
            ))}
            <Typography sx={{ mt: 2 }}>
              Confidence: {(result.confidence * 100).toFixed(1)}%
            </Typography>
          </Paper>
        )}
      </Box>
    </Container>
  );
}

export default App; 