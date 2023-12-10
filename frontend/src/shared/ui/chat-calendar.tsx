import { Box } from '@mui/material';
import { DateCalendar } from '@mui/x-date-pickers';
import React, { useState } from 'react';
import ChatButton from './chat-button';

interface ChatCalendarProps {
  onSelected: (value: Date) => unknown;
}

function ChatCalendar({ onSelected }: ChatCalendarProps) {
  const [value, setValue] = useState();
  return (
    <Box>
      <DateCalendar value={value} onChange={(newValue) => setValue(newValue)} disablePast />
      <ChatButton onClick={() => onSelected(value['$d'])}>Выбрать</ChatButton>
    </Box>
  );
}

export default ChatCalendar;
