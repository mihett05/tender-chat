import { configureStore } from '@reduxjs/toolkit';
import { createContractFormSlice } from '~/widgets/create-contract/lib/slice';
import { chatSlice } from '~/features/chat/lib/slice';

export const store = configureStore({
  reducer: {
    createContractForm: createContractFormSlice.reducer,
    chat: chatSlice.reducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
