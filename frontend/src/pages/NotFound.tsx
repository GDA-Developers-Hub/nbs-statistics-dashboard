import React from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'

const NotFound = () => {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center text-center">
      <h1 className="text-9xl font-extrabold tracking-widest text-gray-900">404</h1>
      <div className="absolute rotate-12 rounded bg-primary px-2 text-sm text-white">
        Page Not Found
      </div>
      <div className="mt-8">
        <p className="text-lg text-gray-600">
          The page you are looking for doesn't exist or has been moved.
        </p>
        <div className="mt-6 flex items-center justify-center gap-4">
          <Button asChild variant="outline">
            <Link to="/">Go Home</Link>
          </Button>
          <Button asChild>
            <Link to="/dashboard">Dashboard</Link>
          </Button>
        </div>
      </div>
    </div>
  )
}

export default NotFound
