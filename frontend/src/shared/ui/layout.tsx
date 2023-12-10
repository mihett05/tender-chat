import React from 'react';
import { Grid } from '@mui/material';

interface LayoutProps {
  children?: React.ReactNode;
  left?: React.ReactNode;
  right?: React.ReactNode;
}

function Layout({ children, left, right }: LayoutProps) {
  return (
    <Grid container>
      {left && <Grid xs={3}>{left}</Grid>}
      <Grid item xs={right ? 6 : 9}>
        {children}
      </Grid>
      {right && <Grid xs={3}>{right}</Grid>}
    </Grid>
  );
}

export default Layout;
