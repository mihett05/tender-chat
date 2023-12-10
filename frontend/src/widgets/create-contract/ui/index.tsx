import React, { useEffect, useState } from 'react';
import { useAppDispatch, useAppSelector } from '~/store';
import { clearForm, setField } from '../lib/slice';
import { addMessage, changeInput, answerMessage, clearChat } from '~/features/chat/lib/slice';
import { createContractForm } from '../lib/form';
import Chat from '~/features/chat/ui/chat';
import { addContract, selectChat } from '~/widgets/contract-chat/lib/slice';
import { useNavigate } from 'react-router-dom';

function CreateContract() {
  const dispatch = useAppDispatch();
  const contractForm = useAppSelector((state) => state.createContractForm);
  const messages = useAppSelector((state) => state.chat);
  const navigate = useNavigate();
  const contracts = useAppSelector((state) => state.contracts.contracts);

  const sendQuestion = () => {
    const field = createContractForm[contractForm.state];
    if (field) {
      dispatch(
        addMessage({
          sender: 0,
          text: field.text,
          buttons: field.buttons,
          calendar: field.calendar,
        }),
      );
      dispatch(
        changeInput({
          format: field.format,
          disabled: field.buttons !== undefined || field.calendar === true,
        }),
      );
    }
  };

  if (messages.messages.length === 0) {
    sendQuestion();
  } else if (messages.messages.length > 1 && contractForm.state === 'federalLaw') {
    dispatch(clearChat());
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

  const dispatchNextState = (value: string, text?: string) => {
    dispatch(
      addMessage({
        sender: currentUserId,
        text: text || value,
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
          if (value === 'Создать') {
            const ids = Object.keys(contracts).sort();
            const id = parseInt(ids[ids.length - 1]) + 1;
            dispatch(
              addContract({
                id: id,
                commits: [
                  {
                    id: 2,
                    senderId: currentUserId,
                    root: true,
                    changes: contractForm.form,
                    status: 'ACCEPTED',
                    messages: [],
                  },
                ],
                contract: contractForm.form,
              }),
            );
            dispatch(clearChat());
            dispatch(clearForm());
            dispatch(selectChat(id));
            navigate(`/chat/${id}`);
          }
        } else {
          dispatch(answerMessage(messageId));
          dispatchNextState(value);
        }
      }}
      onCalendar={(value, messageId) => {
        dispatch(answerMessage(messageId));
        dispatchNextState(value, value.toLocaleDateString());
      }}
      disabled={messages.disabled}
    />
  );
}

export default CreateContract;
