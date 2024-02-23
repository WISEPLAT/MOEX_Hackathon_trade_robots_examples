import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
import * as fs from "fs";
import * as path from 'path';
const __dirname = path.resolve();
const log = debug("emission");

export const createEmission = async ({deep, Types, packageName, packageId}: {
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
  console.log({ContainId, SymbolId, TypeId, StringId, ValueId, NumberId, SyncTextFileId, HandlerId, HandleInsertId, dockerSupportsBunJsId});

  const UnitId = await deep.id('@suenot/unit', 'Unit');
  const WalletId = await deep.id('@suenot/wallet', 'Wallet');

  // Emission
  const { data: [{ id: EmissionId }] } = await deep.insert({
    type_id: TypeId,
    // ASK: можно добавить, что она от Unit к Wallet, а так Any к Any
    // ASK: может эмиссия это просто один из видов транзакций? Но у нее свои хендлеры (она не снимает деньги с ассета, но эту логику можно объединить в одном insert handler)
    from_id: UnitId, // UnitId,
    to_id: WalletId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Emission' } },
      },
    ] },
    out: { data: [
    ] },
  });
  log({EmissionId});

  // SymbolId (петличка от Emission к Emission)
  const { data: [{ id: symbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '🖨️' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'symbol' } },
      },
    ] },
    from_id: EmissionId,
    to_id: EmissionId,
  });
  log({symbolId});

  return {packageId, EmissionId, symbolId};
};

