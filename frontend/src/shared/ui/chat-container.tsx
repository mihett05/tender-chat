import React, { forwardRef } from 'react';
import { Box, Paper } from '@mui/material';

interface ChatContainerProps {
  children: React.ReactNode;
  input?: React.ReactNode;
}

function ChatContainer({ children, input }: ChatContainerProps, ref: React.ForwardedRef<unknown>) {
  return (
    <Box
      sx={{
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        background: 'linear-gradient(to right bottom, #FFFFFF, #48B8C2) !important',
      }}
    >
      <Paper
        sx={{
          height: '100%',
          overflow: 'auto',
          overflowY: 'scroll',
          px: 1,
          borderRadius: 0,
          background: 'linear-gradient(to right bottom, #FFFFFF, #48B8C2) !important',
        }}
        elevation={0}
      >
        <Box
          ref={ref}
          sx={{
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          {children}
        </Box>
      </Paper>
      <Box
        sx={{
          justifyContent: 'flex-end',
        }}
      >
        {input}
      </Box>
    </Box>
  );
}

export default forwardRef(ChatContainer);
