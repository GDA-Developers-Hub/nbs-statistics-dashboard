import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Button, Card, Spinner, Alert, Tabs, Tab, Table } from 'react-bootstrap';

const API_BASE_URL = 'http://localhost:8002/api';

const RealTimeDataPanel = ({ category }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);

  // Function to fetch data from the real-time API
  const fetchData = useCallback(async (triggerUpdate = false) => {
    setLoading(true);
    setError(null);
    
    try {
      // Construct the API URL
      let url = `${API_BASE_URL}/realtime/data/`;
      if (category) {
        url += `${category}/`;
      }
      
      // Add auto_update parameter if needed
      if (triggerUpdate) {
        url += `?auto_update=true`;
      }
      
      // Make the API call
      const response = await axios.get(url);
      
      // Update state with the data
      setData(response.data);
      setLastUpdated(new Date());
      
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
      await axios.post(`${API_BASE_URL}/realtime/trigger/`, {
        categories: categoriesToScrape,
        force: true
      });
      
      // Wait a bit for the scrape to start
      setTimeout(() => {
        // Fetch the updated data
        fetchData();
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

  // Group data by categories
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
        
        {lastUpdated && (
          <div className="text-muted small mb-3">
            Last updated: {lastUpdated.toLocaleTimeString()}
          </div>
        )}
        
        {categoryNames.length === 0 ? (
          <Alert variant="warning">No data categories available</Alert>
        ) : (
          <Tabs defaultActiveKey={categoryNames[0]} className="mb-3">
            {categoryNames.map(catName => (
              <Tab key={catName} eventKey={catName} title={catName.charAt(0).toUpperCase() + catName.slice(1)}>
                <div className="table-responsive">
                  <Table striped hover>
                    <thead>
                      <tr>
                        <th>Dataset</th>
                        <th>Time Period</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {categories[catName].map(item => (
                        <tr key={item.id}>
                          <td>{item.title}</td>
                          <td>{item.time_period || 'N/A'}</td>
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
            ))}
          </Tabs>
        )}
      </Card.Body>
    </Card>
  );
};

export default RealTimeDataPanel; 