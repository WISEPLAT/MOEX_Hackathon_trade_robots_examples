import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
const log = debug("language");

export const createLanguage = async ({deep, Types, packageName, packageId}: {
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

  // Language
  const { data: [{ id: LanguageId }] } = await deep.insert({
    type_id: TypeId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Language' } },
      },
    ] },
    out: { data: [
    ] },
  });
  console.log({LanguageId});

  // SymbolId
  const { data: [{ id: symbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '🌍' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'symbol' } },
      },
    ] },
    from_id: LanguageId,
    to_id: LanguageId,
  });
  console.log({symbolId});

  // languageValue
  const { data: [{ id: languageValueId }] } = await deep.insert({
    type_id: ValueId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'languageValue' } },
      },
    ] },
    from_id: LanguageId,
    to_id: StringId,
  });
  console.log({languageValueId});

  // AvailableLanguage
  const { data: [{ id: AvailableLanguageId }] } = await deep.insert({
    type_id: TypeId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'AvailableLanguage' } },
      },
    ] },
    out: { data: [
    ] },
  });
  console.log({AvailableLanguageId});

  // ActiveLanguage
  const { data: [{ id: ActiveLanguageId }] } = await deep.insert({
    type_id: TypeId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'ActiveLanguage' } },
      },
    ] },
    out: { data: [
    ] },
  });
  console.log({ActiveLanguageId});

  return { packageId, LanguageId, symbolId, languageValueId, AvailableLanguageId, ActiveLanguageId };
};