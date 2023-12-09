import React from 'react';
import { Provider } from 'react-redux';
import { RouterProvider } from 'react-router-dom';

import { store } from '~/store';
import { router } from './router';
import { CssBaseline } from '@mui/material';

function App() {
  return (
    <>
      <CssBaseline />
      <Provider store={store}>
        <RouterProvider router={router} />
      </Provider>
    </>
  );
}

export default App;
