import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import { AddAppointment } from './pages/AddAppointments';
import { ListAppointments } from './pages/ListAppointments';
import { AddPatient } from './pages/AddPatient';

function App() {
    return (
        <Router>
            <div className="container">
                <div className="mb-4">
                    <Link to="/add-appointment" className="btn btn-primary me-2">Agregar Cita</Link>
                    <Link to="/list-appointments" className="btn btn-secondary me-2">Listar Citas</Link>
                    <Link to="/add-patient" className="btn btn-success">Agregar Paciente</Link>
                </div>
                <Routes>
                    <Route path="/add-appointment" element={<AddAppointment />} />
                    <Route path="/list-appointments" element={<ListAppointments />} />
                    <Route path="/add-patient" element={<AddPatient />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
