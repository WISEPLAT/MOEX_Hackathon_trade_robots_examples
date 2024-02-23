import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
const log = debug("task");

export const createTask = async ({deep, Types, packageName, packageId}: {
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

  // Task
  const { data: [{ id: TaskId }] } = await deep.insert({
    type_id: TypeId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Task' } },
      },
    ] },
    out: { data: [
    ] },
  });
  console.log({TaskId});

  // SymbolId
  const { data: [{ id: symbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '📋' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'symbol' } },
      },
    ] },
    from_id: TaskId,
    to_id: TaskId,
  });
  console.log({symbolId});

  // taskValue
  const { data: [{ id: waletValueId }] } = await deep.insert({
    type_id: ValueId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'taskValue' } },
      },
    ] },
    from_id: TaskId,
    to_id: StringId,
  });
  log({waletValueId});

  return { packageId, TaskId, symbolId };
};