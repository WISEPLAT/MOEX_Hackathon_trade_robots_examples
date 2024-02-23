import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
const log = debug("unit-ui-ru");
import * as fs from "fs";
import * as path from 'path';
const __dirname = path.resolve();

export const createUnitUiRu = async ({deep, Types, packageName, packageId}: {
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
    SyncTextFileId
  } = Types;
  log('createUnitUiRu');
  log({packageName, ContainId, SymbolId, TypeId, StringId, ValueId});

  const LocaleId = await deep.id('@suenot/locale', 'Locale');
  log({LocaleId});

  // syncTextFile
  const { data: [{ id: syncTextFile }] } = await deep.insert({
    type_id: SyncTextFileId,
    string: { data: {
      value: fs.readFileSync(path.join(__dirname, 'src', 'unit-ui-ru-locale.ts'), { encoding: 'utf-8' })
    } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'syncTextFile' } },
      },
      {
        type_id: LocaleId,
        from_id: packageId,
        string: { data: { value: 'ru' } },
      },
    ] },
  });
  log({syncTextFile});

  return { packageId };
};