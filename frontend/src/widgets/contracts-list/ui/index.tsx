import { Avatar, Box, Typography, useTheme } from '@mui/material';
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppSelector } from '~/store';

import AddIcon from '~/shared/assets/add.svg?react';

function ContractsList() {
  const theme = useTheme();
  const navigate = useNavigate();
  const contracts = useAppSelector((state) => state.contracts.contracts);

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <div onClick={() => navigate('/create')}>
        <Box
          sx={{
            display: 'flex',
            alignContent: 'space-between',
            alignItems: 'center',
            gap: 3,
            p: 3,
            bgcolor: '#48B8C2',
            cursor: 'pointer',
          }}
        >
          <AddIcon />
          <Typography variant="h5">Добавить заказ</Typography>
        </Box>
      </div>
      {Object.keys(contracts).map((id) => (
        <div onClick={() => navigate(`/chat/${id}`)}>
          <Box
            sx={{
              display: 'flex',
              alignContent: 'space-between',
              alignItems: 'center',
              gap: 3,
              p: 3,
              ':hover': {
                bgcolor: theme.palette.grey[100],
                cursor: 'pointer',
              },
            }}
          >
            <Avatar>N</Avatar>

            <Box>
              <Typography variant="h5">Контракт № {id}</Typography>
              <Typography variant="subtitle1" color="gray">
                До истечения контракта 4 дн.
              </Typography>
            </Box>
          </Box>
        </div>
      ))}
    </Box>
  );
}

export default ContractsList;
