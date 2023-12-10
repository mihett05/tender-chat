import { Box, Divider, Link } from '@mui/material';
import React, { useState } from 'react';
import { Commit } from '~/entities/contract';
import ChatMessage from '~/shared/ui/chat-message';
import { useAppDispatch } from '~/store';
import { selectCommit } from '~/widgets/contract-chat/lib/slice';

interface CommitMessageProps {
  commit: Commit;
  currentUserId: number;
  senderType: 'customer' | 'contractor';
  last?: boolean;
}

function CommitMessage({ commit, currentUserId, senderType, last }: CommitMessageProps) {
  const [open, setOpen] = useState<boolean>(last === undefined ? false : true);
  const dispatch = useAppDispatch();
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <ChatMessage
        align={commit.senderId === currentUserId ? 'right' : 'left'}
        buttons={
          commit.status === 'PROPOSED' && commit.senderId !== currentUserId
            ? {
                Посмотреть: 'view', // view_id
                Принять: 'accept',
                Отклонить: 'decline',
                Контрпредложение: 'proposal',
              }
            : { Посмотреть: 'view' }
        }
        onButtonPressed={(value) => {
          if (value === 'view') {
            dispatch(selectCommit(commit.id));
          }
        }}
      >
        {senderType === 'customer' ? 'Заказчик' : 'Поставщик'} предложил изменения
      </ChatMessage>
      {commit.messages.length > 0 && (
        <Link
          align="center"
          sx={{
            cursor: 'pointer',
          }}
        >
          <a onClick={() => setOpen((state) => !state)}>
            {open ? 'Скрыть' : 'Показать'} комментарии к изменению
          </a>
        </Link>
      )}

      {open &&
        commit.messages.map((message) => (
          <ChatMessage align={message.sender === currentUserId ? 'right' : 'left'}>
            {message.text}
          </ChatMessage>
        ))}
      {!last && (
        <Divider
          sx={{
            mb: 1,
          }}
        />
      )}
    </Box>
  );
}

export default CommitMessage;
