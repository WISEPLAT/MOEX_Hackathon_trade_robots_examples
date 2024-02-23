import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
const log = debug("unit");

export const createUnit = async ({deep, Types, packageName, packageId}: {
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

  // Unit
  const { data: [{ id: UnitId }] } = await deep.insert({
    type_id: TypeId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Unit' } },
      },
    ] },
    out: { data: [
    ] },
  });
  console.log({UnitId});

  // SymbolId
  const { data: [{ id: symbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '💎' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'symbol' } },
      },
    ] },
    from_id: UnitId,
    to_id: UnitId,
  });
  console.log({symbolId});

  return { packageId, UnitId, symbolId };
};