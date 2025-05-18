import React, { useEffect } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: string;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  requiredRole 
}) => {
  const { isAuthenticated, user, checkAuth } = useAuth();
  const location = useLocation();

  useEffect(() => {
    const verifyAuth = async () => {
      await checkAuth();
    };
    
    verifyAuth();
  }, [checkAuth]);

  // If not authenticated, redirect to login
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If a specific role is required, check user's role
  if (requiredRole && user?.role !== requiredRole) {
    // Role check failed - either redirect to dashboard or show unauthorized page
    return <Navigate to="/dashboard" replace />;
  }

  // User is authenticated and has required role (if specified)
  return <>{children}</>;
};

export default ProtectedRoute; 