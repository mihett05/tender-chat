import { Box, useTheme } from '@mui/material';
import React from 'react';
import ChatButton from './chat-button';

interface ChatMessageProps {
  children: React.ReactNode;
  align: 'left' | 'right'; // арабы в пролёте
  buttons?: { [text: string]: string }; // Текст кнопки -> Значение кнопки
  buttonsVariant?: 'column' | 'row';
  onButtonPressed?: (value: string) => unknown;
  disabled?: boolean;
}

function ChatMessage({
  children: text,
  align,
  buttons,
  buttonsVariant,
  onButtonPressed,
  disabled,
}: ChatMessageProps) {
  const theme = useTheme();
  return (
    <Box>
      <Box
        sx={{
          float: align,
        }}
      >
        <Box
          sx={{
            bgcolor: align === 'left' ? theme.palette.secondary.main : theme.palette.primary.main,
            padding: 1,
            borderRadius: theme.shape.borderRadius,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'start',
            color:
              align === 'left'
                ? theme.palette.secondary.contrastText
                : theme.palette.primary.contrastText,
          }}
        >
          {text}
        </Box>
        {!disabled && (
          <Box
            sx={{
              py: 0.5,
              display: 'flex',
              flexDirection: buttonsVariant || 'column',
              alignItems: 'center',
              justifyContent: 'space-between',
              alignContent: 'space-between',
              gap: 0.5,
            }}
          >
            {buttons &&
              Object.entries(buttons).map(([text, value]) => (
                <ChatButton onClick={() => onButtonPressed && onButtonPressed(value)} key={value}>
                  {text}
                </ChatButton>
              ))}
          </Box>
        )}
      </Box>
    </Box>
  );
}

export default ChatMessage;
