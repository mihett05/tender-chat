import React, { useEffect } from 'react';
import ContractView from '~/features/contract-view/ui';
import Layout from '~/shared/ui/layout';
import { useParams } from 'react-router-dom';
import { useAppDispatch } from '~/store';
import ContractChat from '~/widgets/contract-chat/ui';
import { selectChat } from '~/widgets/contract-chat/lib/slice';
import ContractsList from '~/widgets/contracts-list/ui';

function ChatPage() {
  const { chatId } = useParams();
  const dispatch = useAppDispatch();
  useEffect(() => {
    dispatch(selectChat(parseInt(chatId)));
  }, [chatId]);
  return (
    <Layout right={<ContractView />} left={<ContractsList />}>
      <ContractChat />
    </Layout>
  );
}

export default ChatPage;
