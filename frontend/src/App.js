import React, { useState } from 'react';
import { Container, Navbar, Nav, Alert } from 'react-bootstrap';
import RiskAssessment from './components/RiskAssessment';
import PortfolioConfiguration from './components/PortfolioConfiguration';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import 'bootstrap/dist/css/bootstrap.min.css';

const App = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [profileData, setProfileData] = useState(null);
  const [userWeights, setUserWeights] = useState(null);
  const [selectedVariant, setSelectedVariant] = useState('baseline');
  const [error, setError] = useState('');

  const handleProfileGenerated = (data) => {
    setProfileData(data);
    setCurrentStep(2);
    setError('');
  };

  const handleWeightsCalculated = (weights, variant) => {
    setUserWeights(weights);
    setSelectedVariant(variant);
    setCurrentStep(3);
    setError('');
  };

  const handleStartOver = () => {
    setCurrentStep(1);
    setProfileData(null);
    setUserWeights(null);
    setSelectedVariant('baseline');
    setError('');
  };

  const steps = [
    { number: 1, title: 'Risk Assessment', active: currentStep === 1, completed: currentStep > 1 },
    { number: 2, title: 'Portfolio Configuration', active: currentStep === 2, completed: currentStep > 2 },
    { number: 3, title: 'Analytics & Results', active: currentStep === 3, completed: false }
  ];

  return (
    <div className="App">
      {/* Navigation Bar */}
      <Navbar bg="dark" variant="dark" expand="lg" className="shadow-sm">
        <Container>
          <Navbar.Brand href="#" className="fw-bold">
            🎯 Fintellect Risk Profiler
          </Navbar.Brand>
          <Nav className="ms-auto">
            <Nav.Link onClick={handleStartOver} className="text-light">
              Start Over
            </Nav.Link>
          </Nav>
        </Container>
      </Navbar>

      {/* Progress Indicator */}
      <Container className="py-3">
        <div className="d-flex justify-content-center">
          {steps.map((step, index) => (
            <div key={step.number} className="d-flex align-items-center">
              <div className={`rounded-circle d-flex align-items-center justify-content-center ${
                step.active ? 'bg-primary text-white' : 
                step.completed ? 'bg-success text-white' : 
                'bg-light text-muted border'
              }`} style={{ width: '40px', height: '40px' }}>
                {step.completed ? '✓' : step.number}
              </div>
              <div className="ms-2 me-4">
                <small className={step.active ? 'text-primary fw-bold' : 'text-muted'}>
                  {step.title}
                </small>
              </div>
              {index < steps.length - 1 && (
                <div className="border-top" style={{ width: '50px', marginRight: '1rem' }}></div>
              )}
            </div>
          ))}
        </div>
      </Container>

      {/* Global Error Display */}
      {error && (
        <Container>
          <Alert variant="danger" dismissible onClose={() => setError('')}>
            {error}
          </Alert>
        </Container>
      )}

      {/* Main Content */}
      <main>
        {currentStep === 1 && (
          <RiskAssessment 
            onProfileGenerated={handleProfileGenerated}
          />
        )}
        
        {currentStep === 2 && profileData && (
          <PortfolioConfiguration
            profileData={profileData}
            onWeightsCalculated={handleWeightsCalculated}
          />
        )}
        
        {currentStep === 3 && profileData && userWeights && (
          <AnalyticsDashboard
            profileData={profileData}
            userWeights={userWeights}
            selectedVariant={selectedVariant}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-dark text-light py-4 mt-5">
        <Container>
          <div className="text-center">
            <h5>Fintellect Risk Profiler</h5>
            <p className="mb-0">
              <small>
                AI-powered financial risk assessment and portfolio optimization. 
                Built for the Smart India Hackathon 2024.
              </small>
            </p>
          </div>
        </Container>
      </footer>
    </div>
  );
};

export default App;