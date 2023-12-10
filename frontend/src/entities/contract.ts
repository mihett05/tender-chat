import { Message } from './chat';

export type Commit = {
  id: number;
  root: boolean;
  status: 'ACCEPTED' | 'PROPOSED' | 'DECLINE';
  changes: Partial<Contract>;
  senderId: number;
  messages: Message[];
};

export type Contract = {
  federalLaw: string;
  purchaseMethod: string;
  basis: string;
  contractNumber: string;
  endDate: string;
  subject: string;
  address: string;
  purchaseIdentificationCode: string;
  fundingSource: string;
  price: string;
  advance: string;
  inn: string;
  ogrn: string;
  kpp: string;
  factAddress: string;
  bankName: string;
  bik: string;
  bankAccaunt: string;
  phoneNumber: string;
  email: string;
  okpo: string;
  oktmo: string;
  okato: string;
  productName: string;
  units: string;
  priceWithoutVat: string;
  quantity: string;
  // TODO: реквизиты
};
