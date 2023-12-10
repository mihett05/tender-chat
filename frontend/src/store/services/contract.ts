import axios from 'axios';
import { Contract } from '~/entities/contract';

export const createContract = async (contract: Contract) => {
  const result = await axios.post(`http://localhost:8000/chats/create_contract_docs/`, contract);
  return result.data['file_url'];
};
