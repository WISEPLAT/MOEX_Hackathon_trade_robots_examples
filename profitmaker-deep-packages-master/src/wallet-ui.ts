import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
import * as fs from "fs";
import * as path from 'path';
const log = debug("wallet-ui");
const __dirname = path.resolve();

export const createWalletUi = async ({deep, Types, packageName, packageId}: {
  deep: DeepClient,
  packageName: string,
  Types: TypesStore,
  packageId: number,
}) => {
  console.log('createWalletUi')
  const {
    ContainId,
    TsxId,
    clientSupportsJsId,
    HandleClientId,
    HandlerId,
  } = Types;

  // tsxId
  // const reservedIds = await deep.reserve(1);
  const { data: [{ id: tsxId }] } = await deep.insert({
    // id: reservedIds.pop(),
    type_id: TsxId,
    string: {
      data: {
        value: fs.readFileSync(path.join(__dirname, 'src', 'wallet-ui.tsx'), { encoding: 'utf-8' })
      },
    },
    in: {
      data: {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: "walletTsx" } },
      }
    }
  });
  log({tsxId});
  console.log({clientSupportsJsId});
  console.log({HandleClientId});
  console.log({HandlerId});
  const WalletId = await deep.id('@suenot/wallet', 'Wallet');
  console.log({WalletId});

  // handler
  const { data: [{ id: handlerId }] } = await deep.insert({
    type_id: HandlerId,
    in: {
      data: {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: "walletHandler" } },
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
        string: { data: { value: "walletHandleClient" } },
      }
    },
    from_id: WalletId,
    to_id: handlerId,
  });
  log({handleClientId});

  return {packageId, WalletId, tsxId, handlerId, handleClientId};
};