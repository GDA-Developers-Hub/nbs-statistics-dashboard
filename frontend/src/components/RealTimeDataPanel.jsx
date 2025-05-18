import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Button, Card, Spinner, Alert, Tabs, Tab, Table, Badge, Row, Col } from 'react-bootstrap';

const API_BASE_URL = 'http://localhost:8000/api';

const RealTimeDataPanel = ({ category }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);

  // Function to fetch data from the real-time API
  const fetchData = useCallback(async (triggerUpdate = false, forceRefresh = false) => {
    setLoading(true);
    setError(null);
    
    try {
      // Construct the API URL
      let url = `${API_BASE_URL}/realtime/data/`;
      if (category) {
        url += `${category}/`;
      }
      
      // Add query parameters
      const params = [];
      if (triggerUpdate) params.push('auto_update=true');
      if (forceRefresh) params.push('refresh=true');
      
      if (params.length > 0) {
        url += `?${params.join('&')}`;
      }
      
      // Make the API call
      const response = await axios.get(url);
      
      // Update state with the data
      setData(response.data);
      setLastUpdated(new Date());
      
      // Check if a scrape was triggered
      if (response.data.scrape_triggered) {
        console.log('Background scrape has been triggered');
      }
      
    } catch (err) {
      console.error('Error fetching real-time data:', err);
      setError(err.message || 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  }, [category]);

  // Function to manually trigger a scrape
  const triggerScrape = async () => {
    setRefreshing(true);
    
    try {
      // Request categories to scrape
      const categoriesToScrape = category ? [category] : undefined;
      
      // Call the trigger API
      const response = await axios.post(`${API_BASE_URL}/realtime/trigger/`, {
        categories: categoriesToScrape,
        force: true
      });
      
      // Show message about scrape status
      console.log(`Scrape status: ${response.data.status}`);
      
      // Wait a bit for the scrape to start
      setTimeout(() => {
        // Fetch the updated data with forced refresh
        fetchData(true, true);
        setRefreshing(false);
      }, 2000);
      
    } catch (err) {
      console.error('Error triggering scrape:', err);
      setError(err.message || 'Failed to trigger scrape');
      setRefreshing(false);
    }
  };

  // Set up auto-refresh interval
  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(() => {
        fetchData(true);  // Pass true to trigger auto_update
      }, 30000);  // Refresh every 30 seconds
      
      return () => clearInterval(interval);
    }
  }, [autoRefresh, fetchData]);

  // Initial data fetch
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Format date for display
  const formatDate = (isoString) => {
    try {
      const date = new Date(isoString);
      return date.toLocaleString();
    } catch (e) {
      return 'Unknown';
    }
  };

  if (loading && !data) {
    return (
      <div className="text-center p-4">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </div>
    );
  }

  if (error && !data) {
    return (
      <Alert variant="danger">
        Error: {error}
        <Button 
          variant="outline-danger" 
          size="sm" 
          className="ms-2"
          onClick={() => fetchData()}
        >
          Try Again
        </Button>
      </Alert>
    );
  }

  // If we don't have data yet, show a loading message
  if (!data) {
    return <div>No data available</div>;
  }

  // Extract data in the new format
  const categories = data.categories || {};
  const categoryNames = Object.keys(categories);

  return (
    <Card className="shadow-sm">
      <Card.Header className="d-flex justify-content-between align-items-center">
        <h5 className="mb-0">
          {category ? `${category.charAt(0).toUpperCase() + category.slice(1)} Statistics` : 'Somalia Statistics'}
        </h5>
        <div>
          <Button 
            variant={autoRefresh ? "primary" : "outline-primary"} 
            size="sm" 
            className="me-2"
            onClick={() => setAutoRefresh(!autoRefresh)}
          >
            {autoRefresh ? "Auto-Refresh On" : "Auto-Refresh Off"}
          </Button>
          <Button 
            variant="success" 
            size="sm" 
            onClick={triggerScrape}
            disabled={refreshing}
          >
            {refreshing ? (
              <>
                <Spinner 
                  as="span" 
                  animation="border" 
                  size="sm" 
                  role="status" 
                  aria-hidden="true" 
                  className="me-1" 
                />
                Refreshing...
              </>
            ) : 'Refresh Now'}
          </Button>
        </div>
      </Card.Header>
      <Card.Body>
        {loading && (
          <Alert variant="info">
            <Spinner animation="border" size="sm" className="me-2" />
            Updating data...
          </Alert>
        )}
        
        <div className="text-muted small mb-3 d-flex justify-content-between">
          <div>
            Last updated: {lastUpdated ? lastUpdated.toLocaleString() : 'Never'}
          </div>
          <div>
            Job completed: {data.job_completed_at ? formatDate(data.job_completed_at) : 'Unknown'}
          </div>
        </div>
        
        {categoryNames.length === 0 ? (
          <Alert variant="warning">No data categories available</Alert>
        ) : (
          <Tabs defaultActiveKey={categoryNames[0]} className="mb-3">
            {categoryNames.map(catName => {
              const categoryData = categories[catName];
              const summary = categoryData.summary || {};
              const items = categoryData.items || [];
              
              return (
                <Tab key={catName} eventKey={catName} title={catName.charAt(0).toUpperCase() + catName.slice(1)}>
                  {/* Category Summary */}
                  <Card className="mb-3 bg-light">
                    <Card.Body>
                      <Row>
                        <Col md={4}>
                          <h6>Summary</h6>
                          <div><strong>Total Items:</strong> {summary.count || 0}</div>
                          <div><strong>Latest Period:</strong> {summary.latest_period || 'N/A'}</div>
                        </Col>
                        <Col md={8}>
                          {/* Category-specific statistics */}
                          {catName === 'demographics' && summary.total_population && (
                            <div>
                              <Badge bg="info" className="me-2">Population</Badge>
                              {summary.total_population.value.toLocaleString()} ({summary.total_population.year})
                            </div>
                          )}
                          {catName === 'economy' && summary.gdp_growth && (
                            <div>
                              <Badge bg="success" className="me-2">GDP Growth</Badge>
                              {summary.gdp_growth.value}% ({summary.gdp_growth.year})
                            </div>
                          )}
                          {catName === 'inflation' && summary.current_inflation && (
                            <div>
                              <Badge bg="warning" className="me-2">Inflation Rate</Badge>
                              {summary.current_inflation.value}% ({summary.current_inflation.period})
                            </div>
                          )}
                        </Col>
                      </Row>
                    </Card.Body>
                  </Card>
                  
                  {/* Data Table */}
                  <div className="table-responsive">
                    <Table striped hover>
                      <thead>
                        <tr>
                          <th>Dataset</th>
                          <th>Time Period</th>
                          <th>Preview</th>
                          <th>Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {items.map(item => (
                          <tr key={item.id}>
                            <td>{item.title}</td>
                            <td>{item.time_period || 'N/A'}</td>
                            <td>
                              {item.data_preview && (
                                <Button
                                  variant="link"
                                  size="sm"
                                  onClick={() => alert(JSON.stringify(item.data_preview, null, 2))}
                                >
                                  Preview
                                </Button>
                              )}
                            </td>
                            <td>
                              <Button 
                                variant="outline-primary" 
                                size="sm"
                                href={`/dashboard/data/${item.id}`}
                              >
                                View Data
                              </Button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </Table>
                  </div>
                </Tab>
              );
            })}
          </Tabs>
        )}
      </Card.Body>
      <Card.Footer className="text-muted small">
        <div className="d-flex justify-content-between">
          <div>Total Items: {data.total_items || 0}</div>
          <div>Real-time data is {autoRefresh ? 'automatically updated' : 'not auto-updating'}</div>
        </div>
      </Card.Footer>
    </Card>
  );
};

export default RealTimeDataPanel; 