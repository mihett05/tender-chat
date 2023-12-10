import React, { useEffect, useMemo, useState } from 'react';
import Chat from '~/features/chat/ui/chat';
import { useChat } from '~/features/chat/lib/hooks';
import { Format, Message } from '~/entities/chat';
import CreateContract from '~/widgets/create-contract/ui';
import Layout from '~/shared/ui/layout';
import ContractsList from '~/widgets/contracts-list/ui';

// const createMessageFromField = (id: number, field: FormField): Message => ({
//   id,
//   text: field.text,
//   sender: 0,
//   buttons: field.buttons,
// });

// const states: FormState[] = Object.keys(form) as FormState[];

function CreateContractPage() {
  // const [state, setState] = useState<FormState | null>('federalLaw');
  // const [formResult, setFormResult] = useState<Partial<CreateContractForm>>({});
  // const disabled = useMemo(() => state === null || form[state]?.buttons !== undefined, [state]);
  // const { messages, setMessages, format, setFormat, addMessage } = useChat([]);
  // const currentUserId = 1;
  // useEffect(() => {
  //   console.log(state);
  //   if (state !== null) {
  //     sendQuestion(state);
  //   } else {
  //     finish();
  //   }
  // }, [state]);
  // const finish = () => {
  //   console.log('finished');
  //   window.location.reload();
  // };
  // const sendQuestion = (newState: FormState) => {
  //   const field = form[newState];
  //   setFormat(field.format);
  //   addMessage(
  //     createMessageFromField(
  //       messages.length > 0 ? messages[messages.length - 1].id + 1 : 0,
  //       form[newState]!,
  //     ),
  //   );
  // };
  // const nextState = () => {
  //   setState((value) => {
  //     const newState = states[states.indexOf(value!) + 1];
  //     return newState;
  //   });
  // };
  // const sendAnswer = (value: string) => {
  //   setFormResult({
  //     ...formResult,
  //     [state!]: value,
  //   });
  //   if (form[state!]?.buttons !== undefined) {
  //     messages[messages.length - 1].answered = true;
  //   }
  //   addMessage({
  //     id: messages.length > 0 ? messages[messages.length - 1].id + 1 : 0,
  //     text: value,
  //     sender: currentUserId,
  //   });
  //   nextState();
  // };
  // return (
  //   <Chat
  //     messages={messages}
  //     format={format}
  //     addMessage={(value) => {
  //       sendAnswer(value.text);
  //     }}
  //     currentUserId={currentUserId}
  //     onButtonPress={(value) => {
  //       sendAnswer(value);
  //     }}
  //     disabled={disabled}
  //   />
  // );
  return (
    <Layout left={<ContractsList />}>
      <CreateContract />
    </Layout>
  );
}

export default CreateContractPage;
