import { createBrowserRouter, Navigate } from 'react-router-dom';
import { useAuthStore } from '@/store/auth';
import MainLayout from '@/layouts/MainLayout';
import Login from '@/pages/Login';
import Register from '@/pages/Register';
import Dashboard from '@/pages/Dashboard';
import CrawlerList from '@/pages/Crawler/CrawlerList';
import CrawlerCreate from '@/pages/Crawler/CrawlerCreate';
import CrawlerEdit from '@/pages/Crawler/CrawlerEdit';
import CrawlerDetail from '@/pages/Crawler/CrawlerDetail';
import TaskList from '@/pages/Task/TaskList';
import TaskDetail from '@/pages/Task/TaskDetail';
import DataList from '@/pages/Data/DataList';

// Protected route wrapper
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

export const router = createBrowserRouter([
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/register',
    element: <Register />,
  },
  {
    path: '/',
    element: (
      <ProtectedRoute>
        <MainLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: <Navigate to="/dashboard" replace />,
      },
      {
        path: 'dashboard',
        element: <Dashboard />,
      },
      {
        path: 'crawlers',
        children: [
          {
            index: true,
            element: <CrawlerList />,
          },
          {
            path: 'create',
            element: <CrawlerCreate />,
          },
          {
            path: ':id',
            element: <CrawlerDetail />,
          },
          {
            path: ':id/edit',
            element: <CrawlerEdit />,
          },
        ],
      },
      {
        path: 'tasks',
        children: [
          {
            index: true,
            element: <TaskList />,
          },
          {
            path: ':id',
            element: <TaskDetail />,
          },
        ],
      },
      {
        path: 'data',
        element: <DataList />,
      },
    ],
  },
]);
