import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
const log = debug("pair");

export const createPair = async ({deep, Types, packageName, packageId}: {
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

  const UnitId = await deep.id('@suenot/unit', 'Unit');

  console.log({packageName, ContainId, SymbolId, TypeId, StringId, ValueId});

  // Pair
  const { data: [{ id: PairId }] } = await deep.insert({
    type_id: TypeId,
    from_id: UnitId, // Base
    to_id: UnitId, // Quote
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Pair' } },
      },
    ] },
    out: { data: [
    ] },
  });
  console.log({UnitId});

  // SymbolId
  const { data: [{ id: symbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '👫' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'symbol' } },
      },
    ] },
    from_id: PairId,
    to_id: PairId,
  });
  console.log({symbolId});

  return { packageId, PairId, symbolId };
};