import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
const log = debug("exchange");

export const createExchange = async ({deep, Types, packageName, packageId}: {
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
  } = Types;
  console.log({packageName, ContainId, SymbolId, TypeId, StringId, ValueId});

  // Exchange
  const { data: [{ id: ExchangeId }] } = await deep.insert({
    type_id: TypeId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Exchange' } },
      },
    ] },
    out: { data: [
    ] },
  });
  console.log({ExchangeId});

  // SymbolId
  const { data: [{ id: symbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '🏦' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'symbol' } },
      },
    ] },
    from_id: ExchangeId,
    to_id: ExchangeId,
  });
  console.log({symbolId});

  return { packageId, ExchangeId, symbolId };
};