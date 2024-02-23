import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
const log = debug("portfolio");

export const createTransactionTests = async ({deep, Types, packageName, packageId}: {
  deep: DeepClient,
  packageName: string,
  Types: TypesStore,
  packageId: number,
}) => {
  const {
    ContainId,
  } = Types;

  const UnitId = await deep.id('@suenot/unit', 'Unit');
  const UnitNameId = await deep.id('@suenot/unit', 'Name');
  const UnitTickerId = await deep.id('@suenot/unit', 'Ticker');
  const UnitAvatarId = await deep.id('@suenot/unit', 'Avatar');
  const UnitDescriptionId = await deep.id('@suenot/unit', 'Description');
  const WalletId = await deep.id('@suenot/wallet', 'Wallet');
  const WalletNameId = await deep.id('@suenot/wallet', 'Name');
  const WalletDescriptionId = await deep.id('@suenot/wallet', 'Description');
  const WalletAvatarId = await deep.id('@suenot/wallet', 'Avatar');
  const ContainUnitId = await deep.id('@suenot/wallet', 'ContainUnit');
  const TransactionId = await deep.id('@suenot/transaction', 'Transaction');

  console.log({packageName, packageId, UnitId, ContainId, UnitNameId, UnitTickerId, UnitAvatarId, UnitDescriptionId, WalletId, WalletNameId, WalletDescriptionId, WalletAvatarId, ContainUnitId, TransactionId});

  // Создаем unit1
  const { data: [{ id: unitId1 }] } = await deep.insert({
    type_id: UnitId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'unit1' } },
      },
    ] },
    out: { data: [
    ] },
  });
  console.log({unitId1});

  console.log({UnitNameId});

  // Создаем unit1 name
  const { data: [{ id: unit1NameId }] } = await deep.insert({
    type_id: UnitNameId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'unit1Name' } },
      },
    ] },
    from_id: unitId1,
    to_id: unitId1,
    string: { data: { value: 'Dogecoin' } },
  });
  console.log({unit1NameId});

  // Создаем unit1 ticker
  const { data: [{ id: unit1TickerId }] } = await deep.insert({
    type_id: UnitTickerId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'unit1Ticker' } },
      },
    ] },
    out: { data: [
    ] },
    from_id: unitId1,
    to_id: unitId1,
    string: { data: { value: 'DOGE' } },
  });
  console.log({unit1TickerId});

  // Создаем unit1 avatar
  const { data: [{ id: unit1AvatarId }] } = await deep.insert({
    type_id: UnitAvatarId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'unit1Avatar' } },
      },
    ] },
    out: { data: [
    ] },
    from_id: unitId1,
    to_id: unitId1,
    string: { data: { value: 'https://w7.pngwing.com/pngs/305/230/png-transparent-shiba-inu-dogecoin-akita-cryptocurrency-bitcoin-mammal-cat-like-mammal-carnivoran-thumbnail.png' } },
  });
  console.log({unit1AvatarId});

    // Создаем unit1 description
    const { data: [{ id: unit1DescriptionId }] } = await deep.insert({
      type_id: UnitDescriptionId,
      in: { data: [
        {
          type_id: ContainId,
          from_id: packageId,
          string: { data: { value: 'unit1Description' } },
        },
      ] },
      out: { data: [
      ] },
      from_id: unitId1,
      to_id: unitId1,
      string: { data: { value: 'Dogecoin is a popular cryptocurrency that started as a playful meme in 2013. It features the Shiba Inu dog from the "Doge" internet meme as its console.logo. Despite its humorous origins, Dogecoin has gained a dedicated following and is used for tipping content creators, charitable donations, and as a digital currency for various online transactions. It distinguishes itself with a vibrant and welcoming community and relatively low transaction fees.' } },
    });
    console.log({unit1DescriptionId});

  // Создаем wallet1
  const { data: [{ id: walletId1 }] } = await deep.insert({
    type_id: WalletId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'wallet1' } },
      },
    ] },
    out: { data: [
      {
        type_id: ContainUnitId,
        to_id: unitId1,
      }
    ] },
    number: { data: { value: 333 } },
  });
  console.log({walletId1});

  // Создаем wallet1 name
  const { data: [{ id: wallet1NameId }] } = await deep.insert({
    type_id: WalletNameId,
    from_id: walletId1,
    to_id: walletId1,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'wallet1Name' } },
      },
    ] },
    string: { data: { value: "For cat's toys" } },
  });
  console.log({wallet1NameId});

  // Создаем wallet1 description
  const { data: [{ id: wallet1DescriptionId }] } = await deep.insert({
    type_id: WalletDescriptionId,
    from_id: walletId1,
    to_id: walletId1,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'wallet1Description' } },
      },
    ] },
    string: { data: { value: "Buying toys for cats is essential for their physical and mental well-being, and it enhances the quality of their life while fostering a closer connection with their human companions." } },
  });
  console.log({wallet1DescriptionId});

    // Создаем wallet1 avatar
    const { data: [{ id: wallet1AvatarId }] } = await deep.insert({
      type_id: WalletAvatarId,
      from_id: walletId1,
      to_id: walletId1,
      in: { data: [
        {
          type_id: ContainId,
          from_id: packageId,
          string: { data: { value: 'wallet1Avatar' } },
        },
      ] },
      string: { data: { value: "https://github.com/suenot/portfolio-icons/blob/main/cat.jpeg?raw=true" } },
    });
    console.log({wallet1AvatarId});

  // Создаем wallet2
  const { data: [{ id: walletId2 }] } = await deep.insert({
    type_id: WalletId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'walletId2' } },
      },
    ] },
    out: { data: [
      {
        type_id: ContainUnitId,
        to_id: unitId1,
      }
    ] },
    number: { data: { value: 444 } },
  });
  console.log({walletId2});
  

  // Создаем transaction1
  const { data: [{ id: transactionId1 }] } = await deep.insert({
    type_id: TransactionId,
    from_id: walletId1,
    to_id: walletId2,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'transactionId1' } },
      },
    ] },
    out: { data: [
    ] },
    number: { data: { value: 222.00000001 } },
  });
  console.log({transactionId1});

  return {packageId, unitId1, walletId1, walletId2, transactionId1};
};