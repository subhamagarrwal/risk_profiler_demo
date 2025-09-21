import React, { useState, useEffect } from 'react';
import { Container, Card, Row, Col, Badge, Button, Alert, Spinner, Form, Table } from 'react-bootstrap';
import { api } from '../services/api';

const PortfolioConfiguration = ({ profileData, onWeightsCalculated }) => {
  const [selectedVariant, setSelectedVariant] = useState('baseline');
  const [weights, setWeights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const variants = [
    { value: 'defensive', label: 'Defensive', description: 'Lower risk, more bonds and cash' },
    { value: 'baseline', label: 'Baseline', description: 'Balanced approach based on your profile' },
    { value: 'aggressive', label: 'Aggressive', description: 'Higher risk, more equity exposure' }
  ];

  // Load baseline weights on component mount
  useEffect(() => {
    calculateWeights('baseline');
  }, [profileData]);

  const calculateWeights = async (variant) => {
    setLoading(true);
    setError('');

    try {
      const weightsData = await api.calculateWeights(
        profileData.label,
        variant,
        profileData.axes
      );
      setWeights(weightsData);
      setSelectedVariant(variant);
    } catch (err) {
      console.error('Error calculating weights:', err);
      setError(err.response?.data?.detail || 'Failed to calculate portfolio weights.');
    } finally {
      setLoading(false);
    }
  };

  const handleVariantChange = (variant) => {
    calculateWeights(variant);
  };

  const handleProceedToAnalytics = () => {
    if (weights) {
      onWeightsCalculated(weights.weights, selectedVariant);
    }
  };

  const formatPercentage = (value) => `${(value * 100).toFixed(1)}%`;
  const formatAxisValue = (value) => `${(value * 100).toFixed(0)}%`;

  return (
    <Container className="py-5">
      <Row>
        <Col lg={8}>
          <Card className="shadow mb-4">
            <Card.Header className="bg-success text-white">
              <h3 className="mb-0">Your Risk Profile</h3>
            </Card.Header>
            <Card.Body>
              <Row>
                <Col md={6}>
                  <h4>
                    <Badge bg="primary" className="me-2">
                      {profileData.label}
                    </Badge>
                    <small className="text-muted">Score: {profileData.score}/100</small>
                  </h4>
                  <div className="mt-3">
                    <strong>Investment Timeline:</strong> {profileData.profile.timeline_years} years<br />
                    <strong>Loss Aversion:</strong> {profileData.profile.loss_aversion.replace('_', ' ')}<br />
                    <strong>Liquidity Need:</strong> {profileData.profile.liquidity_need}<br />
                    <strong>Income Stability:</strong> {profileData.profile.income_stability}
                  </div>
                </Col>
                <Col md={6}>
                  <h5>Risk Factors</h5>
                  <Table size="sm" striped>
                    <tbody>
                      <tr>
                        <td>Time Horizon</td>
                        <td>{formatAxisValue(profileData.axes.time_horizon)}</td>
                      </tr>
                      <tr>
                        <td>Loss Aversion</td>
                        <td>{formatAxisValue(profileData.axes.loss_aversion)}</td>
                      </tr>
                      <tr>
                        <td>Liquidity Need</td>
                        <td>{formatAxisValue(profileData.axes.liquidity)}</td>
                      </tr>
                      <tr>
                        <td>Income Stability</td>
                        <td>{formatAxisValue(profileData.axes.income_stability)}</td>
                      </tr>
                    </tbody>
                  </Table>
                </Col>
              </Row>
            </Card.Body>
          </Card>

          <Card className="shadow">
            <Card.Header className="bg-info text-white">
              <h3 className="mb-0">Portfolio Configuration</h3>
            </Card.Header>
            <Card.Body>
              {error && (
                <Alert variant="danger" className="mb-4">
                  {error}
                </Alert>
              )}

              <Form.Group className="mb-4">
                <Form.Label className="h5">Select Portfolio Variant:</Form.Label>
                <Row className="g-3">
                  {variants.map((variant) => (
                    <Col md={4} key={variant.value}>
                      <Card 
                        className={`h-100 cursor-pointer ${selectedVariant === variant.value ? 'border-primary bg-light' : ''}`}
                        style={{ cursor: 'pointer' }}
                        onClick={() => !loading && handleVariantChange(variant.value)}
                      >
                        <Card.Body className="text-center">
                          <h5 className={selectedVariant === variant.value ? 'text-primary' : ''}>
                            {variant.label}
                          </h5>
                          <small className="text-muted">{variant.description}</small>
                          {selectedVariant === variant.value && (
                            <Badge bg="primary" className="mt-2">Selected</Badge>
                          )}
                        </Card.Body>
                      </Card>
                    </Col>
                  ))}
                </Row>
              </Form.Group>

              {loading ? (
                <div className="text-center py-4">
                  <Spinner animation="border" />
                  <p className="mt-2">Calculating optimal weights...</p>
                </div>
              ) : weights ? (
                <div>
                  <h5>Recommended Asset Allocation</h5>
                  <Row className="mb-4">
                    {Object.entries(weights.weights).map(([asset, weight]) => (
                      <Col md={4} key={asset} className="mb-3">
                        <Card className="h-100">
                          <Card.Body className="text-center">
                            <h3 className="text-primary">{formatPercentage(weight)}</h3>
                            <h6 className="text-capitalize">{asset}</h6>
                          </Card.Body>
                        </Card>
                      </Col>
                    ))}
                  </Row>

                  {weights.explanations && weights.explanations.length > 0 && (
                    <Alert variant="info">
                      <Alert.Heading className="h6">Portfolio Adjustments:</Alert.Heading>
                      <ul className="mb-0">
                        {weights.explanations.map((explanation, index) => (
                          <li key={index}>{explanation}</li>
                        ))}
                      </ul>
                    </Alert>
                  )}

                  <div className="d-grid">
                    <Button
                      variant="success"
                      size="lg"
                      onClick={handleProceedToAnalytics}
                    >
                      Proceed to Analytics & Backtesting
                    </Button>
                  </div>
                </div>
              ) : (
                <Alert variant="warning">
                  Please wait while we calculate your portfolio weights...
                </Alert>
              )}
            </Card.Body>
          </Card>
        </Col>

        <Col lg={4}>
          <Card className="shadow bg-light">
            <Card.Header>
              <h5 className="mb-0">Understanding Asset Classes</h5>
            </Card.Header>
            <Card.Body>
              <div className="mb-3">
                <h6 className="text-primary">Equity</h6>
                <small>Stock market investments with higher growth potential but more volatility.</small>
              </div>
              <div className="mb-3">
                <h6 className="text-primary">Bonds</h6>
                <small>Government and corporate debt securities providing steady income with lower risk.</small>
              </div>
              <div className="mb-3">
                <h6 className="text-primary">Cash</h6>
                <small>Liquid investments like money market funds for safety and immediate access.</small>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default PortfolioConfiguration;