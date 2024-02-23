import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
import * as fs from "fs";
import * as path from 'path';
const log = debug("unit-ui");
const __dirname = path.resolve();

export const createUnitUi = async ({deep, Types, packageName, packageId}: {
  deep: DeepClient,
  packageName: string,
  Types: TypesStore,
  packageId: number,
}) => {
  const {
    ContainId,
    TsxId,
    clientSupportsJsId,
    HandleClientId,
    HandlerId,
  } = Types;
  console.log({packageName, ContainId, TsxId, clientSupportsJsId, HandleClientId, HandlerId});

  // tsxId
  // const reservedIds = await deep.reserve(1);
  const { data: [{ id: tsxId }] } = await deep.insert({
    // id: reservedIds.pop(),
    type_id: TsxId,
    string: {
      data: {
        value: fs.readFileSync(path.join(__dirname, 'src', 'unit-ui.tsx'), { encoding: 'utf-8' })
      },
    },
    in: {
      data: {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: "unitTsx" } },
      }
    }
  });
  log({tsxId});
  console.log({clientSupportsJsId});
  console.log({HandleClientId});
  console.log({HandlerId});

  const UnitId = await deep.id('@suenot/unit', 'Unit');
  console.log({UnitId});

  // handler
  const { data: [{ id: handlerId }] } = await deep.insert({
    type_id: HandlerId,
    in: {
      data: {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: "unitHandler" } },
      }
    },
    from_id: clientSupportsJsId,
    to_id: tsxId,
  });
  log({handlerId});

  // handleClient
  const { data: [{ id: handleClientId }] } = await deep.insert({
    type_id: HandleClientId,
    in: {
      data: {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: "unitHandleClient" } },
      }
    },
    from_id: UnitId,
    to_id: handlerId,
  });
  log({handleClientId});



  // tsxId
  const { data: [{ id: publicTsxId }] } = await deep.insert({
    type_id: TsxId,
    string: {
      data: {
        value: fs.readFileSync(path.join(__dirname, 'src', 'unit-ui.tsx'), { encoding: 'utf-8' })
      },
    },
    in: {
      data: {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: "publicUnitTsx" } },
      }
    }
  });
  log({publicTsxId});

  // handler
  const { data: [{ id: publicHandlerId }] } = await deep.insert({
    type_id: HandlerId,
    in: {
      data: {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: "publicUnitHandler" } },
      }
    },
    from_id: clientSupportsJsId,
    to_id: tsxId,
  });
  log({publicTsxId});

  // handleClient
  const { data: [{ id: publicHandleClientId }] } = await deep.insert({
    type_id: HandleClientId,
    in: {
      data: {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: "publicUnitHandleClient" } },
      }
    },
    from_id: UnitId,
    to_id: publicHandlerId,
  });
  log({publicHandleClientId});






  // tsxId
  const { data: [{ id: editTsxId }] } = await deep.insert({
    type_id: TsxId,
    string: {
      data: {
        value: fs.readFileSync(path.join(__dirname, 'src', 'unit-ui.tsx'), { encoding: 'utf-8' })
      },
    },
    in: {
      data: {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: "editUnitTsx" } },
      }
    }
  });
  log({editTsxId});

  // handler
  const { data: [{ id: editHandlerId }] } = await deep.insert({
    type_id: HandlerId,
    in: {
      data: {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: "editUnitHandler" } },
      }
    },
    from_id: clientSupportsJsId,
    to_id: tsxId,
  });
  log({editTsxId});

  // handleClient
  const { data: [{ id: editHandleClientId }] } = await deep.insert({
    type_id: HandleClientId,
    in: {
      data: {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: "editUnitHandleClient" } },
      }
    },
    from_id: UnitId,
    to_id: editHandlerId,
  });
  log({editHandleClientId});


  return {packageId, tsxId, handlerId, handleClientId, publicTsxId, publicHandlerId, publicHandleClientId, editTsxId, editHandlerId, editHandleClientId};
};