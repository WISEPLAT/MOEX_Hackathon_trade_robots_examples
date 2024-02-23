import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
const log = debug("locale");

export const createLocale = async ({deep, Types, packageName, packageId}: {
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

  // Locale
  const { data: [{ id: LocaleId }] } = await deep.insert({
    type_id: TypeId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Locale' } },
      },
    ] },
    out: { data: [
    ] },
  });
  console.log({LocaleId});

  // SymbolId
  const { data: [{ id: symbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '🗺️' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'symbol' } },
      },
    ] },
    from_id: LocaleId,
    to_id: LocaleId,
  });
  console.log({symbolId});

  // localeValue
  const { data: [{ id: localeValueId }] } = await deep.insert({
    type_id: ValueId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'localeValue' } },
      },
    ] },
    from_id: LocaleId,
    to_id: StringId,
  });
  console.log({localeValueId});

  // HasLocale
  const { data: [{ id: HasLocaleId }] } = await deep.insert({
    type_id: TypeId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'HasLocale' } },
      },
    ] },
    out: { data: [
    ] },
  });
  console.log({HasLocaleId});

  // UseLocale
  const { data: [{ id: UseLocaleId }] } = await deep.insert({
    type_id: TypeId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'UseLocale' } },
      },
    ] },
    out: { data: [
    ] },
  });
  console.log({UseLocaleId});

  return { packageId, LocaleId, symbolId, HasLocaleId, UseLocaleId };
};