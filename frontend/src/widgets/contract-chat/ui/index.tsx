import React from 'react';
import Chat from '~/features/chat/ui/chat';
import { useAppDispatch, useAppSelector } from '~/store';
import { addMessage } from '../lib/slice';
import ChatMessage from '~/shared/ui/chat-message';
import CommitMessage from '~/features/commit-message/ui';

function ContractChat() {
  const dispatch = useAppDispatch();
  const contract = useAppSelector((state) => state.contracts.contracts[state.contracts.selectedId]);
  const currentUserId = 1;

  return (
    <Chat
      messages={[
        {
          id: 0,
          sender: 0,
          text: 'Заказчик внёс изменения в контракт',
        },
      ]}
      format="string"
      addMessage={(message) => {
        dispatch(
          addMessage({
            ...message,
          }),
        );
      }}
      currentUserId={currentUserId}
    >
      {contract.commits.map((commit, i) => (
        <CommitMessage
          commit={commit}
          senderType="customer"
          currentUserId={currentUserId}
          last={i === contract.commits.length - 1}
        />
      ))}
    </Chat>
  );
}

export default ContractChat;
