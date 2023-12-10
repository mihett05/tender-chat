import React, { useMemo, useState } from 'react';
import { IconButton, InputAdornment, InputBase, Paper, useTheme } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import type { Format } from '~/entities/chat';

interface ChatInputProps<T> {
  format?: Format;
  disabled?: boolean;
  onSubmit?: (value: T) => unknown;
  placeholder?: string;
}

const FORMAT_TO_TEXT = {
  string: 'Введите сообщение...',
  numeric: '10',
  money: '1.250.00,00',
};

const FORMAT_TO_REGEX = {
  string: /.*/,
  numeric: /^\d+$/,
  money: /^[\d.]+(\,\d*)?$/,
};

function ChatInput<T = string>({ format, disabled, onSubmit, placeholder }: ChatInputProps<T>) {
  const realFormat = format || 'string';
  const text = placeholder || FORMAT_TO_TEXT[realFormat];

  const theme = useTheme();
  const [value, setValue] = useState<string>('');
  const isValid = useMemo(
    () => value.length === 0 || FORMAT_TO_REGEX[realFormat].test(value),
    [value, format],
  );

  return (
    <Paper
      component="form"
      sx={{
        p: '2px 4px',
        display: 'flex',
        alignItems: 'center',
        bgcolor: theme.palette.grey[100],
        borderRadius: theme.shape.borderRadius,
        border: `1px solid ${isValid ? theme.palette.grey[100] : theme.palette.error.main}`,
      }}
      elevation={0}
      onSubmit={(e) => {
        e.preventDefault();
        if (value.length > 0 && isValid) {
          if (onSubmit) {
            onSubmit(realFormat === 'string' ? (value as T) : (parseFloat(value) as T));
          }

          setValue('');
        } else {
        }
      }}
    >
      <InputBase
        value={value}
        onChange={(e) => setValue(e.target.value)}
        sx={{
          ml: 1,
          flex: 1,
          color: isValid
            ? theme.palette.getContrastText(theme.palette.grey[100])
            : theme.palette.error.main,
        }}
        disabled={disabled}
        placeholder={text}
        inputProps={{
          'aria-label': 'отправить сообщение',
        }}
        startAdornment={
          format === 'money' && (
            <InputAdornment
              position="start"
              sx={{
                userSelect: 'none',
                cursor: 'default',
              }}
            >
              ₽
            </InputAdornment>
          )
        }
      />

      <IconButton
        color="primary"
        sx={{ p: '10px' }}
        aria-label="отправить"
        type="submit"
        disabled={disabled}
      >
        <SendIcon />
      </IconButton>
    </Paper>
  );
}

export default ChatInput;
