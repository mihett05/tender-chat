import React, { forwardRef } from 'react';
import { Box, Container, Paper } from '@mui/material';

interface ChatContainerProps {
  children: React.ReactNode;
  input?: React.ReactNode;
}

function ChatContainer({ children, input }: ChatContainerProps, ref: React.ForwardedRef<unknown>) {
  return (
    <Container>
      <Box
        sx={{
          height: '100vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
        }}
      >
        <Paper
          sx={{
            height: '100%',
            overflow: 'auto',
            overflowY: 'scroll',
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
    </Container>
  );
}

export default forwardRef(ChatContainer);
