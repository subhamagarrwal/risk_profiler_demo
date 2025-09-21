import React, { useState } from 'react';
import { Container, Card, Form, Button, Alert, Spinner, Row, Col, ProgressBar } from 'react-bootstrap';
import { api } from '../services/api';

const RiskAssessment = ({ onProfileGenerated }) => {
  const [answers, setAnswers] = useState({
    answer1: '',
    answer2: '',
    answer3: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const questions = [
    {
      id: 'answer1',
      text: 'If your portfolio dropped 20% in a year, what would you do?',
      placeholder: 'e.g., I would hold but feel stressed, I would panic and sell, I would buy more...'
    },
    {
      id: 'answer2', 
      text: 'What excites you more: steady growth or high gains with volatility?',
      placeholder: 'e.g., Prefer steady growth with some risk, Love high gains despite volatility...'
    },
    {
      id: 'answer3',
      text: 'Any large cash needs in the next 2-3 years?',
      placeholder: 'e.g., Down payment in ~3 years, No major expenses planned, Wedding next year...'
    }
  ];

  const handleInputChange = (questionId, value) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate all answers are provided
    if (!answers.answer1 || !answers.answer2 || !answers.answer3) {
      setError('Please answer all three questions.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const profileData = await api.generateProfile(answers);
      onProfileGenerated(profileData);
    } catch (err) {
      console.error('Error generating profile:', err);
      setError(
        err.response?.data?.detail || 
        'Failed to generate risk profile. Please ensure the Ollama service is running and try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const isFormComplete = answers.answer1 && answers.answer2 && answers.answer3;
  const completedAnswers = Object.values(answers).filter(answer => answer.trim() !== '').length;

  return (
    <Container className="py-5">
      <Row className="justify-content-center">
        <Col lg={8}>
          <Card className="shadow-lg">
            <Card.Header className="bg-primary text-white">
              <h2 className="mb-0">Risk Assessment</h2>
              <small>Help us understand your investment preferences</small>
            </Card.Header>
            <Card.Body>
              <ProgressBar 
                now={(completedAnswers / 3) * 100} 
                label={`${completedAnswers}/3 Questions`}
                className="mb-4"
              />

              {error && (
                <Alert variant="danger" className="mb-4">
                  {error}
                </Alert>
              )}

              <Form onSubmit={handleSubmit}>
                {questions.map((question, index) => (
                  <Form.Group key={question.id} className="mb-4">
                    <Form.Label className="h5 text-primary">
                      {index + 1}. {question.text}
                    </Form.Label>
                    <Form.Control
                      as="textarea"
                      rows={3}
                      placeholder={question.placeholder}
                      value={answers[question.id]}
                      onChange={(e) => handleInputChange(question.id, e.target.value)}
                      disabled={loading}
                      className="form-control-lg"
                    />
                  </Form.Group>
                ))}

                <div className="d-grid">
                  <Button 
                    variant="primary" 
                    size="lg" 
                    type="submit" 
                    disabled={!isFormComplete || loading}
                  >
                    {loading ? (
                      <>
                        <Spinner
                          as="span"
                          animation="border"
                          size="sm"
                          role="status"
                          aria-hidden="true"
                          className="me-2"
                        />
                        Analyzing Your Profile...
                      </>
                    ) : (
                      'Generate Risk Profile'
                    )}
                  </Button>
                </div>
              </Form>

              {loading && (
                <Alert variant="info" className="mt-3">
                  <small>
                    <strong>Please wait:</strong> We're using AI to analyze your responses and create your personalized risk profile. This may take up to 2 minutes.
                  </small>
                </Alert>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default RiskAssessment;