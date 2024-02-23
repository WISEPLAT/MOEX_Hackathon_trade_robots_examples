import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
import * as fs from "fs";
import * as path from 'path';
const __dirname = path.resolve();
const log = debug("payment-provider");

export const createPaymentProvider = async ({deep, Types, packageName, packageId}: {
  deep: DeepClient,
  packageName: string,
  Types: TypesStore,
  packageId: number,
}) => {
  const {
    ContainId,
    SymbolId,
    TypeId,
    StringId,
    ValueId,
    NumberId,
    SyncTextFileId,
    HandlerId,
    HandleInsertId,
    HandleUpdateId,
    dockerSupportsBunJsId,
  } = Types;
  console.log({packageName, ContainId, SymbolId, TypeId, StringId, ValueId, NumberId, SyncTextFileId, HandlerId, HandleInsertId, dockerSupportsBunJsId});

  // const WalletId = await deep.id('@suenot/wallet', 'Wallet');
  // const PaymentId = await deep.id('@deep-foundation/payments', 'Payment');
  const PayId = await deep.id('@deep-foundation/payments', 'Pay');
  // const SumId = await deep.id('@deep-foundation/payments', 'Sum');
  // const PayedId = await deep.id('@deep-foundation/payments', 'Payed');
  // const ObjectId = await deep.id('@deep-foundation/payments', 'Object');
  // const StorageId = await deep.id('@deep-foundation/payments', 'Storage');
  // const UrlId = await deep.id('@deep-foundation/payments', 'Url');

  // Transaction

  // syncTextFile
  const { data: [{ id: syncTextFile }] } = await deep.insert({
    type_id: SyncTextFileId,
    string: { data: {
      value: fs.readFileSync(path.join(__dirname, 'src', 'payment-insert-handler.ts'), { encoding: 'utf-8' })
    } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'paymentSyncTextFile' } },
      },
    ] },
  });
  log({syncTextFile});

  // handler
  const { data: [{ id: handlerId }] } = await deep.insert({
    type_id: HandlerId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'paymentHandler' } },
      },
    ] },
    from_id: dockerSupportsBunJsId,
    to_id: syncTextFile,
  });
  log({handlerId});

  // handleInsert
  const { data: [{ id: handleInsertId }] } = await deep.insert({
    type_id: HandleInsertId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'paymentHandleInsert' } },
      },
    ] },
    from_id: PayId,
    to_id: handlerId,
  });
  log({handleInsertId});

  // handleUpdate
  const { data: [{ id: handleUpdateId }] } = await deep.insert({
    type_id: HandleUpdateId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'paymentHandleUpdate' } },
      },
    ] },
    from_id: PayId,
    to_id: handlerId,
  });
  log({handleUpdateId});

  return {packageId, syncTextFile, handlerId};
};

