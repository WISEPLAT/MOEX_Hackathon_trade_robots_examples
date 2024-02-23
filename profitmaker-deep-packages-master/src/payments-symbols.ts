import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
import * as fs from "fs";
import * as path from 'path';
const __dirname = path.resolve();
const log = debug("payments-symbols");

export const createPaymentsSymbols = async ({deep, Types, packageName, packageId}: {
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

  const PaymentId = await deep.id('@deep-foundation/payments', 'Payment');
  const PayId = await deep.id('@deep-foundation/payments', 'Pay');
  const SumId = await deep.id('@deep-foundation/payments', 'Sum');
  const PayedId = await deep.id('@deep-foundation/payments', 'Payed');
  const ObjectId = await deep.id('@deep-foundation/payments', 'Object');
  const StorageId = await deep.id('@deep-foundation/payments', 'Storage');
  const UrlId = await deep.id('@deep-foundation/payments', 'Url');

  const { data: [{ id: paymentSymbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '🐪' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'symbol' } },
      },
    ] },
    from_id: PaymentId,
    to_id: PaymentId,
  });
  log({paymentSymbolId});

  const { data: [{ id: sumSymbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '💰' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'symbol' } },
      },
    ] },
    from_id: SumId,
    to_id: SumId,
  });
  log({sumSymbolId});

  const { data: [{ id: paySymbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '💡' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'symbol' } },
      },
    ] },
    from_id: PayId,
    to_id: PayId,
  });
  log({paySymbolId});

  return {packageId, paymentSymbolId, sumSymbolId, paySymbolId};
};

