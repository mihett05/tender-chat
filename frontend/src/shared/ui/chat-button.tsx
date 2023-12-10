import React from 'react';
import { Button, useTheme } from '@mui/material';

interface ChatButtonProps {
  children: React.ReactNode;
  onClick: () => unknown;
}

function ChatButton({ children: text, onClick: onPress }: ChatButtonProps) {
  const theme = useTheme();
  return (
    <Button
      onClick={onPress}
      variant="outlined"
      sx={{
        textTransform: 'none',
        px: 1,
        py: 0.5,
        width: '100%',
        bgcolor: theme.palette.secondary.main,
        color: theme.palette.text.primary,
        borderRadius: 10,
        boxShadow: 10,
      }}
    >
      {text}
    </Button>
  );
}

export default ChatButton;
