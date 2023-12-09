import React, { useEffect, useRef } from 'react';
import ChatContainer from '~/shared/ui/chat-container';
import ChatInput from '~/shared/ui/chat-input';
import ChatMessage from '~/shared/ui/chat-message';
import { Format, Message } from '~/entities/chat';

interface ChatProps {
  messages: Message[];
  format: Format;
  addMessage: (value: Omit<Message, 'id'>) => unknown;
  currentUserId: number;
  onButtonPress?: (value: string, messageId: number) => unknown;
  disabled?: boolean;
}

function Chat({ messages, format, addMessage, currentUserId, onButtonPress, disabled }: ChatProps) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref !== null) {
      ref.current?.lastElementChild?.scrollIntoView();
    }
  }, [ref, messages]);

  return (
    <ChatContainer
      ref={ref}
      input={
        <ChatInput
          disabled={disabled}
          format={format}
          onSubmit={(value) => {
            if (addMessage) {
              addMessage({
                sender: currentUserId,
                text: value,
              });
            }
          }}
        />
      }
    >
      {messages.map((message) => (
        <ChatMessage
          key={message.id}
          children={message.text}
          align={message.sender === currentUserId ? 'right' : 'left'}
          buttons={message.buttons}
          disabled={message.answered}
          onButtonPressed={(value) => {
            onButtonPress && onButtonPress(value, message.id);
          }}
        />
      ))}
    </ChatContainer>
  );
}

export default Chat;
