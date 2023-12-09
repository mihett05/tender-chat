import React from 'react';
import { Box, Button } from '@mui/material';

interface FormProps {
  children: React.ReactNode;
  onSubmit: () => unknown;
  inputText?: string;
}

function Form({ children, inputText, onSubmit }: FormProps) {
  return (
    <form onSubmit={onSubmit}>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          maxWidth: '20vw',
          padding: '1.5rem',
          justifyContent: 'space-between',
          gap: '1rem',
        }}
      >
        {children}
        <Button
          type="submit"
          variant="contained"
          sx={{
            py: 1,
          }}
        >
          {inputText || 'Отправить'}
        </Button>
      </Box>
    </form>
  );
}

export default Form;
