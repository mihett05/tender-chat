import { Paper, Typography } from '@mui/material';
import React from 'react';
import Layout from '~/shared/ui/layout';
import ContractsList from '~/widgets/contracts-list/ui';

function ListPage() {
  return (
    <Layout left={<ContractsList />}>
      <Paper
        sx={{
          height: '100vh',
          borderRadius: 0,
          background: 'linear-gradient(to right bottom, #DB2B21, #48B8C2) !important',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
        elevation={0}
      >
        <Typography>Выберите чат или создайте новый заказ</Typography>
      </Paper>
    </Layout>
  );
}

export default ListPage;
