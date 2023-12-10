import React from 'react';
import { createBrowserRouter } from 'react-router-dom';
import ChatPage from '~/pages/chat';
import CreateContractPage from '~/pages/create-contract';
import ListPage from '~/pages/list';

import LoginPage from '~/pages/login';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <ListPage />,
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/chat/:chatId',
    element: <ChatPage />,
  },
  {
    path: '/create',
    element: <CreateContractPage />,
  },
]);
