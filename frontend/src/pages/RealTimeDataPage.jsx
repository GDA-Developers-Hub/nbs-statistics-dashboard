import React, { useState } from 'react';
import { Container, Row, Col, Form, Card, Button, Badge, Alert } from 'react-bootstrap';
import RealTimeDataPanel from '../components/RealTimeDataPanel';

const RealTimeDataPage = () => {
  const [selectedCategory, setSelectedCategory] = useState('');
  const categories = [
    { value: '', label: 'All Categories' },
    { value: 'demographics', label: 'Demographics', description: 'Population statistics by region and gender' },
    { value: 'economy', label: 'Economy', description: 'GDP, employment, trade data, and economic indicators' },
    { value: 'health', label: 'Health', description: 'Mortality rates, healthcare access, and vaccination coverage' },
    { value: 'education', label: 'Education', description: 'Literacy rates, school enrollment, and education metrics' },
    { value: 'inflation', label: 'Inflation', description: 'Consumer Price Index and monthly inflation rates' }
  ];

  // Find the currently selected category object
  const selectedCategoryObj = categories.find(cat => cat.value === selectedCategory) || categories[0];

  return (
    <Container fluid className="py-4">
      <Row className="mb-4">
        <Col>
          <h1>
            Real-Time Somalia Statistics
            <Badge bg="success" className="ms-2 fs-6">Live Data</Badge>
          </h1>
          <p className="text-muted">
            Latest data automatically refreshed from the Somalia National Bureau of Statistics
          </p>
        </Col>
      </Row>
      
      <Row className="mb-4">
        <Col md={4}>
          <Card className="shadow-sm">
            <Card.Header className="bg-primary text-white">
              <h5 className="mb-0">Filter Data</h5>
            </Card.Header>
            <Card.Body>
              <Form>
                <Form.Group className="mb-3">
                  <Form.Label>Category</Form.Label>
                  <Form.Select 
                    value={selectedCategory}
                    onChange={(e) => setSelectedCategory(e.target.value)}
                  >
                    {categories.map(cat => (
                      <option key={cat.value} value={cat.value}>
                        {cat.label}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
                
                {selectedCategory && (
                  <Alert variant="info" className="p-2 small">
                    <strong>{selectedCategoryObj.label}:</strong> {selectedCategoryObj.description}
                  </Alert>
                )}
                
                <div className="d-grid">
                  <Button 
                    variant="outline-secondary"
                    onClick={() => setSelectedCategory('')}
                  >
                    Reset Filters
                  </Button>
                </div>
              </Form>
            </Card.Body>
          </Card>
          
          <Card className="shadow-sm mt-4">
            <Card.Header className="bg-dark text-white">
              <h5 className="mb-0">About Real-Time Data</h5>
            </Card.Header>
            <Card.Body>
              <p>
                This page displays the latest statistics from Somalia, refreshed automatically every 20 minutes from official sources.
              </p>
              
              <h6 className="mt-3">Data Features:</h6>
              <ul className="small">
                <li><strong>Auto-Refresh:</strong> Toggle automatic updates every 30 seconds</li>
                <li><strong>Manual Refresh:</strong> Force an immediate data refresh</li>
                <li><strong>Data Preview:</strong> Quick look at the data without loading the full view</li>
                <li><strong>Category Filtering:</strong> Focus on specific types of statistics</li>
              </ul>
              
              <h6 className="mt-3">Available Categories:</h6>
              <ul className="small">
                <li><strong>Demographics:</strong> Population statistics by region, age, and gender</li>
                <li><strong>Economy:</strong> GDP, employment, trade, and economic indicators</li>
                <li><strong>Health:</strong> Mortality rates, healthcare access, vaccination coverage</li>
                <li><strong>Education:</strong> Literacy, enrollment, education quality metrics</li>
                <li><strong>Inflation:</strong> CPI, monthly inflation rates, price trends</li>
              </ul>
            </Card.Body>
            <Card.Footer className="text-center">
              <small className="text-muted">Data source: Somalia National Bureau of Statistics</small>
            </Card.Footer>
          </Card>
        </Col>
        
        <Col md={8}>
          <Alert variant="success" className="mb-3">
            <strong>Real-Time Updates Active:</strong> Data is automatically scraped from source every 20 minutes and displayed here with the latest statistics.
          </Alert>
          <RealTimeDataPanel category={selectedCategory} />
          
          <Card className="shadow-sm mt-4">
            <Card.Header>
              <h5 className="mb-0">How It Works</h5>
            </Card.Header>
            <Card.Body>
              <p>
                The real-time data system uses a sophisticated scraping engine that runs on a 20-minute schedule to extract the latest statistics from the Somalia National Bureau of Statistics website.
              </p>
              <p>
                Data is processed, categorized, and made available through our API. The system includes:
              </p>
              <ul>
                <li><strong>Automated Scraping:</strong> Regular data collection with smart throttling</li>
                <li><strong>Intelligent Caching:</strong> Performance optimization to reduce load</li>
                <li><strong>Category Extraction:</strong> Automatic organization of data by type</li>
                <li><strong>Time-Series Processing:</strong> Historical data tracking and comparison</li>
              </ul>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default RealTimeDataPage; 