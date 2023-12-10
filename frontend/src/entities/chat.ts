export type Message = {
  id: number;
  text: string;
  sender: number;
  buttons?: {
    [key: string]: string;
  };
  answered?: boolean;
  calendar?: boolean;
};

export type Chat = {
  messages: Message[];
};

export type Format = 'string' | 'numeric' | 'money';
