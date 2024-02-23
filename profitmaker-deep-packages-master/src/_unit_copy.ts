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

  // Name
  const { data: [{ id: NameId }] } = await deep.insert({
    type_id: TypeId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Name' } },
      },
    ] },
    from_id: UnitId,
    to_id: UnitId,
  });
  console.log({NameId});

  // nameSymbol (петличка от Name к Name)
  const { data: [{ id: nameSymbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '🔤' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'nameSymbol' } },
      },
    ] },
    from_id: NameId,
    to_id: NameId,
  });
  console.log({nameSymbolId});

  // nameValue
  const { data: [{ id: nameValueId }] } = await deep.insert({
    type_id: ValueId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'nameValue' } },
      },
    ] },
    from_id: NameId,
    to_id: StringId,
  });
  console.log({nameValueId});

  // Ticker
  const { data: [{ id: TickerId }] } = await deep.insert({
    type_id: TypeId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Ticker' } },
      },
    ] },
    from_id: UnitId,
    to_id: UnitId,
  });
  console.log({TickerId});

  // tickerSymbol
  const { data: [{ id: tickerSymbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '📛' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'tickerSymbol' } },
      },
    ] },
    from_id: TickerId,
    to_id: TickerId,
  });
  console.log({tickerSymbolId});

  // tickerValue
  const { data: [{ id: tickerValueId }] } = await deep.insert({
    type_id: ValueId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'tickerValue' } },
      },
    ] },
    from_id: TickerId,
    to_id: StringId,
  });
  console.log({tickerValueId});

  // Avatar
  const { data: [{ id: AvatarId }] } = await deep.insert({
    type_id: TypeId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Avatar' } },
      },
    ] },
    from_id: UnitId,
    to_id: UnitId,
  });
  console.log({AvatarId});

  // avatarSymbol
  const { data: [{ id: avatarSymbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '🖼️' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'avatarSymbol' } },
      },
    ] },
    from_id: AvatarId,
    to_id: AvatarId,
  });
  console.log({avatarSymbolId});

  // avatarValue
  const { data: [{ id: avatarValueId }] } = await deep.insert({
    type_id: ValueId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'avatarValue' } },
      },
    ] },
    from_id: AvatarId,
    to_id: StringId,
  });
  console.log({avatarValueId});

  // Description
  const { data: [{ id: DescriptionId }] } = await deep.insert({
    type_id: TypeId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Description' } },
      },
    ] },
    from_id: UnitId,
    to_id: UnitId,
  });
  console.log({DescriptionId});

  // descriptionSymbol
  const { data: [{ id: descriptionSymbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '✍️' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'descriptionSymbol' } },
      },
    ] },
    from_id: DescriptionId,
    to_id: DescriptionId,
  });
  console.log({descriptionSymbolId});

  // descriptionValue
  const { data: [{ id: descriptionValueId }] } = await deep.insert({
    type_id: ValueId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'descriptionValue' } },
      },
    ] },
    from_id: DescriptionId,
    to_id: StringId,
  });
  console.log({descriptionValueId});

  return { packageId, UnitId, symbolId, NameId, nameSymbolId, TickerId, tickerSymbolId, AvatarId, avatarSymbolId, avatarValueId, DescriptionId, descriptionSymbolId, descriptionValueId };
};