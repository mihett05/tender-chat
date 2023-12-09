import React, { useEffect, useState } from 'react';
import { useAppDispatch, useAppSelector } from '~/store';
import { setField } from '../lib/slice';
import { addMessage, changeInput, answerMessage } from '~/features/chat/lib/slice';
import { createContractForm } from '../lib/form';
import Chat from '~/features/chat/ui/chat';

function CreateContract() {
  const dispatch = useAppDispatch();
  const contractForm = useAppSelector((state) => state.createContractForm);
  const messages = useAppSelector((state) => state.chat);

  const sendQuestion = () => {
    const field = createContractForm[contractForm.state];
    if (field) {
      dispatch(
        addMessage({
          sender: 0,
          text: field.text,
          buttons: field.buttons,
        }),
      );
      dispatch(
        changeInput({
          format: field.format,
          disabled: field.buttons !== undefined,
        }),
      );
    }
  };

  if (messages.messages.length === 0) {
    sendQuestion();
  }

  useEffect(() => {
    if (contractForm.state !== 'federalLaw' && !contractForm.finished) {
      sendQuestion();
    }
  }, [contractForm.state]);

  useEffect(() => {
    if (contractForm.finished) {
      dispatch(
        addMessage({
          sender: 0,
          text: 'Создать договор о закупке?',
          buttons: {
            Создать: 'Создать',
            Отменить: 'Отменить',
          },
        }),
      );
      dispatch(
        changeInput({
          format: 'string',
          disabled: true,
        }),
      );
    }
  }, [contractForm.finished]);

  const currentUserId = 1;

  const dispatchNextState = (value: string) => {
    dispatch(
      addMessage({
        sender: currentUserId,
        text: value,
      }),
    );
    dispatch(setField(value));
  };

  return (
    <Chat
      messages={messages.messages}
      format={messages.format}
      addMessage={(value) => {
        dispatchNextState(value.text);
      }}
      currentUserId={currentUserId}
      onButtonPress={(value, messageId) => {
        if (contractForm.finished) {
          console.log(contractForm);
        } else {
          dispatch(answerMessage(messageId));
          dispatchNextState(value);
        }
      }}
      disabled={messages.disabled}
    />
  );
}

export default CreateContract;
