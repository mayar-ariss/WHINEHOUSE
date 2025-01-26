import React, { useState } from 'react';

const App = () => {
    const [patient, setPatient] = useState({ needs: '', location: '' });
    const [matches, setMatches] = useState([]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setPatient({ ...patient, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch('http://localhost:5000/api/match', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(patient),
        });
        const data = await response.json();
        setMatches(data);
    };

    return (
        <div>
            <h1>RehabMatch</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="needs"
                    placeholder="Needs (e.g., PT, OT)"
                    value={patient.needs}
                    onChange={handleChange}
                />
                <input
                    type="text"
                    name="location"
                    placeholder="Location"
                    value={patient.location}
                    onChange={handleChange}
                />
                <button type="submit">Find Matches</button>
            </form>
            <ul>
                {matches.map((match) => (
                    <li key={match.id}>{match.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default App;
