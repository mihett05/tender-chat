import { Box, useTheme } from '@mui/material';
import React from 'react';
import ChatButton from './chat-button';
import ChatCalendar from './chat-calendar';

interface ChatMessageProps {
  children: React.ReactNode;
  align: 'left' | 'right'; // арабы в пролёте
  buttons?: { [text: string]: string }; // Текст кнопки -> Значение кнопки
  calendar?: boolean;
  buttonsVariant?: 'column' | 'row';
  onButtonPressed?: (value: string) => unknown;
  onCalendar?: (value: Date) => unknown;
  disabled?: boolean;
}

function ChatMessage({
  children: text,
  align,
  buttons,
  buttonsVariant,
  onButtonPressed,
  disabled,
  calendar,
  onCalendar,
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
            bgcolor: align === 'left' ? theme.palette.primary.main : theme.palette.secondary.main,
            padding: 2,
            borderRadius: align === 'left' ? '10px 10px 10px 0' : '10px 10px 0 10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'start',
            color: theme.palette.text.primary,
            boxShadow: 10,
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
            {calendar && <ChatCalendar onSelected={(value) => onCalendar && onCalendar(value)} />}
          </Box>
        )}
      </Box>
    </Box>
  );
}

export default ChatMessage;
