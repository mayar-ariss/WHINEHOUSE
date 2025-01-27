const express = require('express');
const cors = require('cors'); // Import the cors package

const app = express();

app.use(cors()); // Enable CORS for all routes
app.use(express.json()); // Middleware to parse JSON

// Mock database
const facilities = [{ id: 1, name: "Rehab A", location: "City X", services: ["PT", "OT"] }];
const patients = [{ id: 1, name: "John Doe", needs: ["PT"], location: "City Y" }];

// API route for matching
app.post('/api/match', (req, res) => {
    const patient = req.body;
    const matches = facilities.filter(f =>
        patient.needs.every(need => f.services.includes(need))
    );
    res.json(matches);
});

// Start server
app.listen(3000, () => console.log('Server running on port 3000'));
