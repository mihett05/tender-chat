import {
  createApi,
  buildCreateApi,
  fetchBaseQuery,
  BaseQueryFn,
  FetchArgs,
  FetchBaseQueryError,
} from '@reduxjs/toolkit/query/react';

import { RootState } from '../store';
import type { User } from '~/entities/User';

interface LoginRequest {
  username: string;
  password: string;
}

type LoginResponse = User & { token: string };

const baseApiQuery = fetchBaseQuery({
  baseUrl: 'https://dummyjson.com/',
});
export const baseAuthQuery: BaseQueryFn<string | FetchArgs, unknown, FetchBaseQueryError> = async (
  args,
  api,
  extraOptions,
) => {
  let result = await baseApiQuery(args, api, extraOptions);
  if (result.error && result.error.status === 401) {
    const refresh = await baseApiQuery('auth/refresh', api, extraOptions);
    if (refresh.data) {
    }
  }
};

export const api = createApi({
  baseQuery: fetchBaseQuery({
    baseUrl: 'https://dummyjson.com/auth/',
  }),
  endpoints: (builder) => ({
    login: builder.mutation<LoginResponse, LoginRequest>({
      query: (credentials) => ({
        url: 'login',
        method: 'POST',
        body: credentials,
      }),
    }),
  }),
});

export const { useLoginMutation } = api;
