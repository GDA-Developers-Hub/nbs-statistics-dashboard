import React, { useState } from 'react';
import { Container, Row, Col, Form, Card, Button } from 'react-bootstrap';
import RealTimeDataPanel from '../components/RealTimeDataPanel';

const RealTimeDataPage = () => {
  const [selectedCategory, setSelectedCategory] = useState('');
  const categories = [
    { value: '', label: 'All Categories' },
    { value: 'demographics', label: 'Demographics' },
    { value: 'economy', label: 'Economy' },
    { value: 'health', label: 'Health' },
    { value: 'education', label: 'Education' },
    { value: 'inflation', label: 'Inflation' }
  ];

  return (
    <Container fluid className="py-4">
      <Row className="mb-4">
        <Col>
          <h1>Real-Time Somalia Statistics</h1>
          <p className="text-muted">
            Latest data scraped from the Somalia National Bureau of Statistics
          </p>
        </Col>
      </Row>
      
      <Row className="mb-4">
        <Col md={4}>
          <Card className="shadow-sm">
            <Card.Header>
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
            <Card.Header>
              <h5 className="mb-0">About Real-Time Data</h5>
            </Card.Header>
            <Card.Body>
              <p>
                This page displays the latest statistics from Somalia, refreshed automatically at regular intervals.
              </p>
              <p>
                Data is scraped from official sources and processed to provide up-to-date insights on key indicators.
              </p>
              <ul>
                <li>Demographics: Population statistics</li>
                <li>Economy: GDP, employment, trade</li>
                <li>Health: Mortality rates, healthcare access</li>
                <li>Education: Literacy, enrollment</li>
                <li>Inflation: Consumer Price Index</li>
              </ul>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={8}>
          <RealTimeDataPanel category={selectedCategory} />
        </Col>
      </Row>
    </Container>
  );
};

export default RealTimeDataPage; 