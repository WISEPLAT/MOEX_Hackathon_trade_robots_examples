import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
const log = debug("instrument");

export const createInstrument = async ({deep, Types, packageName, packageId}: {
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

  const PairId = await deep.id('@suenot/pair', 'Pair');
  const ExchangeId = await deep.id('@suenot/exchange', 'Exchange');

  console.log({packageName, ContainId, SymbolId, TypeId, StringId, ValueId});

  // Instrument
  const { data: [{ id: InstrumentId }] } = await deep.insert({
    type_id: TypeId,
    from_id: ExchangeId,
    to_id: PairId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Instrument' } },
      },
    ] },
    out: { data: [
    ] },
  });
  console.log({InstrumentId});

  // SymbolId
  const { data: [{ id: symbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '🎹' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'symbol' } },
      },
    ] },
    from_id: InstrumentId,
    to_id: InstrumentId,
  });
  console.log({symbolId});

  return { packageId, InstrumentId, symbolId };
};