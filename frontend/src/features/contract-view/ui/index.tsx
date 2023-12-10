import React, { useEffect, useState } from 'react';
import { Commit, Contract } from '~/entities/contract';
import {
  Divider,
  MenuItem,
  Select,
  TextField,
  Typography,
  useTheme,
  Paper,
  Button,
  Box,
} from '@mui/material';
import { useAppDispatch, useAppSelector } from '~/store';
import { addCommit } from '~/widgets/contract-chat/lib/slice';

const applyChanges = (commit: Commit, commits: Commit[]) => {
  const commitIndex = commits.indexOf(commit);
  let contract = {};

  if (commitIndex === 0) return commit.changes;
  for (let index = 0; index < commitIndex; index++) {
    console.log(commit);
    if (commit.status === 'ACCEPTED' || commit.status === 'PROPOSED') {
      contract = {
        ...contract,
        ...commits[index].changes,
      };
    }
  }
  return contract;
};

const hasChanges = (obj1: any, obj2: any) => {
  return !Object.keys(obj1)
    .map((key) => obj1[key] === obj2[key])
    .every((value) => value);
};

const diff = (obj1: any, obj2: any) => {
  return Object.keys(obj1)
    .filter((key) => obj1[key] !== obj2[key])
    .reduce(
      (prev, curr) => ({
        ...prev,
        [curr]: obj2[curr],
      }),
      {},
    );
};

function ContractView() {
  const theme = useTheme();
  const contracts = useAppSelector((state) => state.contracts);
  const contract = useAppSelector((state) => state.contracts.contracts[state.contracts.selectedId]);
  const commit = useAppSelector((state) =>
    state.contracts.contracts[state.contracts.selectedId].commits.find(
      (c) => c.id === state.contracts.selectedCommitId,
    ),
  );

  const dispatch = useAppDispatch();

  const getStyles = (field: string) => ({
    bgcolor: !commit?.root && commit?.changes[field] ? theme.palette.success.light : 'initial',
    color: !commit?.root && commit?.changes[field] ? theme.palette.success.contrastText : 'initial',
  });

  const onChange = (field: string) => (e) =>
    setValues({
      ...values,
      [field]: e.target.value,
    });

  const appliedChanges = applyChanges(commit!, contract.commits);

  const [values, setValues] = useState<Partial<Contract>>(appliedChanges);

  useEffect(() => {
    setValues({
      ...appliedChanges,
      ...commit!.changes,
    });
  }, [commit]);
  return (
    <Paper
      sx={{
        height: '100vh',
        overflow: 'auto',
        overflowY: 'scroll',
      }}
    >
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          width: '100%',
        }}
      >
        <Button
          variant="contained"
          sx={{
            width: '100%',
            m: 2,
          }}
          disabled={
            !(
              commit?.status === 'ACCEPTED' &&
              hasChanges(values, { ...appliedChanges, ...commit!.changes })
            )
          }
          onClick={() => {
            dispatch(
              addCommit({
                id: contract.commits[contract.commits.length - 1].id + 1,
                messages: [],
                senderId: 1,
                status: 'PROPOSED',
                changes: diff({ ...appliedChanges, ...commit!.changes }, values),
                root: false,
              }),
            );
          }}
        >
          Отправить на рассмотрение
        </Button>
      </Box>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          width: '100%',
        }}
      >
        <Button
          variant="contained"
          sx={{
            width: '100%',
            m: 2,
          }}
          color="secondary"
          onClick={() => {}}
        >
          Открыть контракт
        </Button>
      </Box>
      <table>
        <tbody>
          <tr>
            <td>Статус</td>
            <td>
              {commit?.status === 'PROPOSED' ? (
                <p
                  style={{
                    color: theme.palette.primary.main,
                  }}
                >
                  Предложено
                </p>
              ) : commit?.status === 'ACCEPTED' ? (
                <p style={{ color: theme.palette.success.light }}>Принято</p>
              ) : (
                <p style={{ color: theme.palette.error.light }}>Отклонено</p>
              )}
            </td>
          </tr>
          <tr>
            <td>Номер</td>
            <td>
              <TextField
                value={values.contractNumber}
                onChange={onChange('contractNumber')}
                InputProps={{
                  sx: getStyles('contractNumber'),
                }}
              />
            </td>
          </tr>
          <tr>
            <td>ФЗ</td>
            <td>
              <Select
                value={values.federalLaw}
                onChange={onChange('federalLaw')}
                sx={getStyles('federalLaw')}
              >
                <MenuItem value="44">44</MenuItem>
                <MenuItem value="224">224</MenuItem>
              </Select>
            </td>
          </tr>
          <tr>
            <td>Метод размещения покупки</td>
            <td>
              <Select
                value={values.purchaseMethod}
                onChange={onChange('purchaseMethod')}
                sx={getStyles('purchaseMethod')}
              >
                <MenuItem value={`В рамках проекта используется только "Единственный поставщик"`}>
                  В рамках проекта используется только "Единственный поставщик"
                </MenuItem>
              </Select>
            </td>
          </tr>
          <tr>
            <td>Основание заключения</td>
            <td>
              <Select value={values.basis} onChange={onChange('basis')} sx={getStyles('basis')}>
                <MenuItem value="п. 4 ч. 1 ст. 93 Закупка объемом до 600 тысяч рублей">
                  п. 4 ч. 1 ст. 93 Закупка объемом до 600 тысяч рублей
                </MenuItem>
                <MenuItem value="п. 4 ч. 1 ст. 93 Закупка объемом до 600 тысяч рублей">
                  п. 5 ч. 1 ст. 93 Закупка объёмом до 600 тысяч рублей
                </MenuItem>
              </Select>
            </td>
          </tr>
          <tr>
            <td>Дата окончание жизни заказа</td>
            <td>
              <TextField
                value={values.endDate}
                onChange={onChange('endDate')}
                InputProps={{
                  sx: getStyles('endDate'),
                }}
              />
            </td>
          </tr>
          <tr>
            <td>Предмет контракта</td>
            <td>
              <TextField
                value={values.subject}
                onChange={onChange('subject')}
                InputProps={{
                  sx: getStyles('subject'),
                }}
              />
            </td>
          </tr>
          <tr>
            <td>Адрес</td>
            <td>
              <TextField
                value={values.address}
                onChange={onChange('address')}
                InputProps={{
                  sx: getStyles('address'),
                }}
              />
            </td>
          </tr>
          <tr>
            <td>ИКЗ</td>
            <td>
              <TextField
                value={values.purchaseIdentificationCode}
                onChange={onChange('purchaseIdentificationCode')}
                InputProps={{
                  sx: getStyles('purchaseIdentificationCode'),
                }}
              />
            </td>
          </tr>
          <tr>
            <td>Источник финансирования</td>
            <td>
              <Select
                value={values.fundingSource}
                onChange={onChange('fundingSource')}
                sx={getStyles('fundingSource')}
              >
                <MenuItem value="Бюджетные средства">Бюджетные средства</MenuItem>
                <MenuItem value="Небюджетные средства">Небюджетные средства</MenuItem>
                <MenuItem value="Средства ОМС">Средства ОМС</MenuItem>
              </Select>
            </td>
          </tr>
          <tr>
            <td>Цена</td>
            <td>
              <TextField
                value={values.price}
                onChange={onChange('price')}
                InputProps={{
                  sx: getStyles('price'),
                }}
              />
            </td>
          </tr>
          <tr>
            <td>Аванс</td>
            <td>
              <TextField
                value={values.advance}
                onChange={onChange('advance')}
                InputProps={{
                  sx: getStyles('advance'),
                }}
              />
            </td>
          </tr>

          <tr>
            <td>ИНН</td>
            <td>
              <TextField
                value={values.inn}
                onChange={onChange('inn')}
                InputProps={{
                  sx: getStyles('inn'),
                }}
              />
            </td>
          </tr>
          <tr>
            <td>КПП</td>
            <td>
              <TextField
                value={values.kpp}
                onChange={onChange('kpp')}
                InputProps={{
                  sx: getStyles('kpp'),
                }}
              />
            </td>
          </tr>
          <tr>
            <td>ОРГН</td>
            <td>
              <TextField
                value={values.ogrn}
                onChange={onChange('orgn')}
                InputProps={{
                  sx: getStyles('orgn'),
                }}
              />
            </td>
          </tr>
          <tr>
            <td>Фактический адрес</td>
            <td>
              <TextField
                value={values.factAddress}
                onChange={onChange('factAddress')}
                InputProps={{
                  sx: getStyles('factAddress'),
                }}
              />
            </td>
          </tr>
          <br />
          <tr>
            <td>
              <Typography variant="h5">Реквизиты</Typography>
            </td>
          </tr>
          <br />
          <tr>
            <td>Наименование банка</td>
            <td>
              <TextField
                value={values.bankName}
                onChange={onChange('bankname')}
                InputProps={{
                  sx: getStyles('bankname'),
                }}
              />
            </td>
          </tr>
          <tr>
            <td>БИК</td>
            <td>
              <TextField
                value={values.bik}
                onChange={onChange('bik')}
                InputProps={{
                  sx: getStyles('bik'),
                }}
              />
            </td>
          </tr>
          <tr>
            <td>Расчётный счёт</td>
            <td>
              <TextField
                value={values.bankAccaunt}
                onChange={onChange('bankAccaunt')}
                InputProps={{
                  sx: getStyles('bankAccaunt'),
                }}
              />
            </td>
          </tr>
          <br />
          <tr>
            <td>
              <Typography variant="h5">Спецификация</Typography>
            </td>
          </tr>
          <tr>
            <td>Наименование продукции</td>
            <td>
              <TextField
                value={values.productName}
                onChange={onChange('productName')}
                InputProps={{
                  sx: getStyles('productName'),
                }}
              />
            </td>
          </tr>
          <tr>
            <td>Единицы измерения</td>
            <td>
              <TextField
                value={values.units}
                onChange={onChange('units')}
                InputProps={{
                  sx: getStyles('units'),
                }}
              />
            </td>
          </tr>
          <tr>
            <td>Цена за единицу</td>
            <td>
              <TextField
                value={values.priceWithoutVat}
                onChange={onChange('priceWithoutVat')}
                InputProps={{
                  sx: getStyles('priceWithoutVat'),
                }}
              />
            </td>
          </tr>
          <tr>
            <td>Количество продукции</td>
            <td>
              <TextField
                value={values.quantity}
                onChange={onChange('quantity')}
                InputProps={{
                  sx: getStyles('quantity'),
                }}
              />
            </td>
          </tr>
          <br />
        </tbody>
      </table>
    </Paper>
  );
}

export default ContractView;
