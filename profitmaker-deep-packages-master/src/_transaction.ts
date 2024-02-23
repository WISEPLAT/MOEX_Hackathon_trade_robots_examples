import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
import * as fs from "fs";
import * as path from 'path';
const __dirname = path.resolve();
const log = debug("transaction");

export const createTransaction = async ({deep, Types, packageName, packageId}: {
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

  const WalletId = await deep.id('@suenot/wallet', 'Wallet');
  const PaymentId = await deep.id('@deep-foundation/payments', 'Payment');
  const PayId = await deep.id('@deep-foundation/payments', 'Pay');
  const SumId = await deep.id('@deep-foundation/payments', 'Sum');
  const PayedId = await deep.id('@deep-foundation/payments', 'Payed');
  const ObjectId = await deep.id('@deep-foundation/payments', 'Object');
  const StorageId = await deep.id('@deep-foundation/payments', 'Storage');
  const UrlId = await deep.id('@deep-foundation/payments', 'Url');

  // Transaction
  const { data: [{ id: TransactionId }] } = await deep.insert({
    type_id: PaymentId, // Наследуем от Payment
    from_id: WalletId,
    to_id: WalletId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Transaction' } },
      },
    ] },
    out: { data: [
    ] },
  });
  log({TransactionId});

  // SymbolId (петличка от Transaction к Transaction)
  const { data: [{ id: symbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '🐪' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'symbol' } },
      },
    ] },
    from_id: TransactionId,
    to_id: TransactionId,
  });
  log({symbolId});

  return {packageId, TransactionId};
};

