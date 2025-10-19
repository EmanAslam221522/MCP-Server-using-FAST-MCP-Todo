const express = require('express');
const cors = require('cors');
const app = express();
const port = 5001;

// Enable CORS for all origins
app.use(cors());
app.use(express.json());

// API endpoint
app.get('/api/message', (req, res) => {
  res.json({
    message: 'Hello from Express Backend!',
    timestamp: new Date().toISOString(),
    status: 'success'
  });
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.listen(port, () => {
  console.log(`Backend API running on port ${port}`);
});