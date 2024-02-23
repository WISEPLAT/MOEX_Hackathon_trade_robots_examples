import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
const log = debug("wallet");

export const createWallet = async ({deep, Types, packageName, packageId}: {
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
  } = Types;

  const UnitId = await deep.id('@suenot/unit', 'Unit');

  // Wallet
  const { data: [{ id: WalletId }] } = await deep.insert({
    type_id: TypeId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Wallet' } },
      },
    ] },
    out: { data: [
    ] },
  });
  log({WalletId});

  // waletValue
  const { data: [{ id: waletValueId }] } = await deep.insert({
    type_id: ValueId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'waletValue' } },
      },
    ] },
    from_id: WalletId,
    to_id: NumberId,
  });
  log({waletValueId});

  // SymbolId (петличка от Unit к Unit)
  const { data: [{ id: symbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '👛' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'symbol' } },
      },
    ] },
    from_id: WalletId,
    to_id: WalletId,
  });
  log({symbolId});

  // ContainUnit
  const { data: [{ id: ContainUnitId }] } = await deep.insert({
    type_id: TypeId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'ContainUnit' } },
      },
    ] },
    from_id: WalletId,
    to_id: UnitId,
  });
  log({ContainUnitId});

  return {packageId, WalletId, waletValueId, symbolId, ContainUnitId};
};