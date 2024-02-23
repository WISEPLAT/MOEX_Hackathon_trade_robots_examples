import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
const log = debug("emission-tests");

export const createEmissionTests = async ({deep, Types, packageName, packageId}: {
  deep: DeepClient,
  packageName: string,
  Types: TypesStore,
  packageId: number,
}) => {
  const {
    ContainId,
  } = Types;
  
  const UnitId = await deep.id('@suenot/unit', 'Unit');
  const WalletId = await deep.id('@suenot/wallet', 'Wallet');
  const EmissionId = await deep.id('@suenot/emission', 'Emission');

  console.log({packageName, packageId, ContainId, UnitId, WalletId, EmissionId});

  // Создаем unit1
  const { data: [{ id: unitId1 }] } = await deep.insert({
    type_id: UnitId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'unitId1' } },
      },
    ] },
    out: { data: [
    ] },
  });
  console.log({unitId1});

  // Создаем wallet1
  const { data: [{ id: walletId1 }] } = await deep.insert({
    type_id: WalletId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'walletId1' } },
      },
    ] },
    out: { data: [
    ] },
  });
  console.log({walletId1});

  // Создаем emission1
  const { data: [{ id: emissionId1 }] } = await deep.insert({
    type_id: EmissionId,
    from_id: unitId1,
    to_id: walletId1,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'emissionId1' } },
      },
    ] },
    number: { data: { value: 999.99 } },
  });
  console.log({emissionId1});

  return {packageId, unitId1, walletId1, emissionId1};
};