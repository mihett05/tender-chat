import { TextField, Typography } from '@mui/material';
import React from 'react';
import { Controller, SubmitHandler, useForm } from 'react-hook-form';
import Form from '~/shared/ui/form';

interface LoginFormInput {
  username: string;
  password: string;
}

function LoginForm() {
  const { control, handleSubmit } = useForm<LoginFormInput>({
    defaultValues: {
      username: '',
      password: '',
    },
  });

  const onSubmit: SubmitHandler<LoginFormInput> = (data) => {
    console.log(data);
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Typography variant="h4" align="center">
        Вход в аккаунт
      </Typography>
      <Controller
        name="username"
        control={control}
        render={({ field }) => <TextField inputProps={field} label="Логин" />}
      />
      <Controller
        name="password"
        control={control}
        render={({ field }) => <TextField inputProps={field} type="password" label="Пароль" />}
      />
    </Form>
  );
}

export default LoginForm;
