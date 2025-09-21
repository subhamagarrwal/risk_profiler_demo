import React, { useState, useEffect } from 'react';
import { Container, Card, Row, Col, Table, Alert, Spinner, Button } from 'react-bootstrap';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { api } from '../services/api';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const AnalyticsDashboard = ({ profileData, userWeights, selectedVariant }) => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    runAnalytics();
  }, [profileData, userWeights]);

  const runAnalytics = async () => {
    setLoading(true);
    setError('');

    try {
      const data = await api.runAnalytics(userWeights, profileData.label, profileData.axes);
      setAnalyticsData(data);
    } catch (err) {
      console.error('Error running analytics:', err);
      setError(err.response?.data?.detail || 'Failed to run portfolio analytics.');
    } finally {
      setLoading(false);
    }
  };

  const formatPercentage = (value) => `${value.toFixed(2)}%`;
  const formatCurrency = (value) => `₹${value.toFixed(2)}`;

  // Chart colors for different portfolios
  const chartColors = {
    'Your Mix': '#007bff',
    'Defensive': '#28a745', 
    'Aggressive': '#dc3545',
    '60/40': '#6f42c1',
    'All Equity': '#fd7e14'
  };

  const createChartConfig = (chartData, title, yAxisLabel) => ({
    data: {
      labels: chartData[Object.keys(chartData)[0]]?.dates || [],
      datasets: Object.entries(chartData).map(([name, data]) => ({
        label: name,
        data: data.values,
        borderColor: chartColors[name] || '#6c757d',
        backgroundColor: `${chartColors[name] || '#6c757d'}20`,
        tension: 0.1,
        pointRadius: 0,
        pointHoverRadius: 4,
      }))
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: title,
          font: { size: 16, weight: 'bold' }
        },
        legend: {
          position: 'bottom',
        },
        tooltip: {
          mode: 'index',
          intersect: false,
        }
      },
      scales: {
        x: {
          display: true,
          title: {
            display: true,
            text: 'Date'
          }
        },
        y: {
          display: true,
          title: {
            display: true,
            text: yAxisLabel
          }
        }
      },
      interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false
      }
    }
  });

  if (loading) {
    return (
      <Container className="py-5">
        <div className="text-center">
          <Spinner animation="border" size="lg" />
          <h3 className="mt-3">Running Portfolio Analytics...</h3>
          <p className="text-muted">
            This may take a few moments as we backtest your portfolio against historical market data.
          </p>
        </div>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="py-5">
        <Alert variant="danger">
          <Alert.Heading>Analytics Error</Alert.Heading>
          {error}
          <hr />
          <Button variant="outline-danger" onClick={runAnalytics}>
            Retry Analytics
          </Button>
        </Alert>
      </Container>
    );
  }

  if (!analyticsData) {
    return (
      <Container className="py-5">
        <Alert variant="warning">No analytics data available.</Alert>
      </Container>
    );
  }

  return (
    <Container fluid className="py-4">
      <Row>
        <Col>
          <h2 className="mb-4">Portfolio Analytics Dashboard</h2>
        </Col>
      </Row>

      {/* Performance Metrics Table */}
      <Row className="mb-5">
        <Col>
          <Card className="shadow">
            <Card.Header className="bg-primary text-white">
              <h4 className="mb-0">Performance Comparison</h4>
            </Card.Header>
            <Card.Body>
              <div className="table-responsive">
                <Table striped bordered hover>
                  <thead>
                    <tr>
                      <th>Portfolio</th>
                      <th>CAGR</th>
                      <th>Volatility</th>
                      <th>Max Drawdown</th>
                      <th>Worst 12M</th>
                      <th>Recovery Time</th>
                    </tr>
                  </thead>
                  <tbody>
                    {analyticsData.portfolios.map((portfolio) => (
                      <tr key={portfolio.name} className={portfolio.name === 'Your Mix' ? 'table-primary' : ''}>
                        <td>
                          <strong>{portfolio.name}</strong>
                          {portfolio.name === 'Your Mix' && (
                            <small className="text-muted d-block">
                              ({selectedVariant} variant)
                            </small>
                          )}
                        </td>
                        <td>{formatPercentage(portfolio.metrics.CAGR_pct)}</td>
                        <td>{formatPercentage(portfolio.metrics.Vol_ann_pct)}</td>
                        <td className="text-danger">{formatPercentage(portfolio.metrics.MaxDD_pct)}</td>
                        <td className="text-danger">{formatPercentage(portfolio.metrics.Worst_12m_pct)}</td>
                        <td>{portfolio.metrics.Recovery_m ? `${portfolio.metrics.Recovery_m} months` : 'N/A'}</td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Charts Row */}
      <Row className="mb-5">
        <Col lg={6}>
          <Card className="shadow h-100">
            <Card.Header className="bg-success text-white">
              <h5 className="mb-0">Investment Growth</h5>
              <small>Growth of ₹1 invested</small>
            </Card.Header>
            <Card.Body>
              <div style={{ height: '400px' }}>
                <Line {...createChartConfig(analyticsData.growth_chart, '', 'Portfolio Value (₹)')} />
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col lg={6}>
          <Card className="shadow h-100">
            <Card.Header className="bg-warning text-dark">
              <h5 className="mb-0">Drawdown Analysis</h5>
              <small>Peak-to-trough declines</small>
            </Card.Header>
            <Card.Body>
              <div style={{ height: '400px' }}>
                <Line {...createChartConfig(analyticsData.drawdown_chart, '', 'Drawdown (%)')} />
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Portfolio Explanations */}
      <Row className="mb-5">
        <Col>
          <Card className="shadow">
            <Card.Header className="bg-info text-white">
              <h4 className="mb-0">Portfolio Analysis</h4>
            </Card.Header>
            <Card.Body>
              <Row>
                {analyticsData.portfolios.map((portfolio) => (
                  <Col md={6} lg={4} key={portfolio.name} className="mb-4">
                    <Card className={portfolio.name === 'Your Mix' ? 'border-primary' : 'border-secondary'}>
                      <Card.Header className={portfolio.name === 'Your Mix' ? 'bg-primary text-white' : 'bg-secondary text-white'}>
                        <h6 className="mb-0">{portfolio.name}</h6>
                      </Card.Header>
                      <Card.Body>
                        <div className="mb-2">
                          <strong>Allocation:</strong>
                          <ul className="mt-1 mb-2">
                            {Object.entries(portfolio.weights).map(([asset, weight]) => (
                              <li key={asset}>
                                {asset}: {formatPercentage(weight * 100)}
                              </li>
                            ))}
                          </ul>
                        </div>
                        <small className="text-muted">
                          {portfolio.explanation.replace(/\*\*/g, '')}
                        </small>
                      </Card.Body>
                    </Card>
                  </Col>
                ))}
              </Row>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Comparisons */}
      {analyticsData.comparisons && analyticsData.comparisons.length > 0 && (
        <Row>
          <Col>
            <Card className="shadow">
              <Card.Header className="bg-secondary text-white">
                <h4 className="mb-0">Key Insights</h4>
              </Card.Header>
              <Card.Body>
                {analyticsData.comparisons.map((comparison, index) => (
                  <Alert key={index} variant="light" className="border-left-primary">
                    {comparison}
                  </Alert>
                ))}
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}
    </Container>
  );
};

export default AnalyticsDashboard;