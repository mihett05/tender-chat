import React from 'react';
import { createBrowserRouter } from 'react-router-dom';
import ChatPage from '~/pages/chat';
import CreateContractPage from '~/pages/create-contract';

import LoginPage from '~/pages/login';

export const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/',
    element: <ChatPage />,
  },
  {
    path: '/create',
    element: <CreateContractPage />,
  },
]);
