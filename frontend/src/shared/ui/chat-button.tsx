import React from 'react';
import { Button } from '@mui/material';

interface ChatButtonProps {
  children: React.ReactNode;
  onClick: () => unknown;
}

function ChatButton({ children: text, onClick: onPress }: ChatButtonProps) {
  return (
    <Button
      onClick={onPress}
      variant="outlined"
      sx={{
        textTransform: 'none',
        px: 1,
        py: 0.5,
        width: '100%',
      }}
    >
      {text}
    </Button>
  );
}

export default ChatButton;
