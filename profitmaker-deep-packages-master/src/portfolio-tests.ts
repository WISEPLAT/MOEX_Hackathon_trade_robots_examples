import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
const log = debug("portfolio-tests");

export const createPortfolioTests = async ({deep, Types, packageName, packageId}: {
  deep: DeepClient,
  packageName: string,
  Types: TypesStore,
  packageId: number,
}) => {
  const {
    ContainId,
  } = Types;

  const UnitId = await deep.id('@suenot/unit', 'Unit');
  const NameId = await deep.id('@suenot/name', 'Name');
  const TickerId = await deep.id('@suenot/ticker', 'Ticker');
  const AvatarId = await deep.id('@suenot/avatar', 'Avatar');
  const DescriptionId = await deep.id('@suenot/description', 'Description');
  const WalletId = await deep.id('@suenot/wallet', 'Wallet');
  const ContainUnitId = await deep.id('@suenot/wallet', 'ContainUnit');

  const UnitUiPackageId = await deep.id('@suenot/unit-ui');
  const WalletUiPackageId = await deep.id('@suenot/wallet-ui');
  const PaymentUiPackageId = await deep.id('@suenot/payment-ui');

  console.log({packageName, ContainId, UnitId, NameId, TickerId, AvatarId, DescriptionId, WalletId, ContainUnitId});

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

  // Создаем unit1 name
  const { data: [{ id: unit1NameId }] } = await deep.insert({
    type_id: NameId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'unit1NameId' } },
      },
    ] },
    from_id: unitId1,
    to_id: unitId1,
    string: { data: { value: 'Dogecoin' } },
  });
  console.log({unit1NameId});

  // Создаем unit1 ticker
  const { data: [{ id: unit1TickerId }] } = await deep.insert({
    type_id: TickerId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'unit1TickerId' } },
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
    type_id: AvatarId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'unit1AvatarId' } },
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
      type_id: DescriptionId,
      in: { data: [
        {
          type_id: ContainId,
          from_id: packageId,
          string: { data: { value: 'unit1DescriptionId' } },
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
        string: { data: { value: 'walletId1' } },
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

  const PortfolioId = await deep.id('@suenot/portfolio', 'Portfolio');
  const ContainWalletId = await deep.id('@suenot/portfolio', 'ContainWallet');

  // Создаем portfolio1
  const { data: [{ id: portfolio1Id }] } = await deep.insert({
    type_id: PortfolioId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'portfolio1Id' } },
      },
    ] },
    out: { data: [
      {
        type_id: ContainWalletId,
        to_id: walletId1,
      },
      {
        type_id: ContainWalletId,
        to_id: walletId2,
      }
    ] },
  });
  console.log({portfolio1Id});

  // Unit ui
  const { data: [{ id: dependenceUnitUi }] } = await deep.insert({
    type_id: ContainId,
    from_id: packageId,
    to_id: UnitUiPackageId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'dependenceUnitUi' } },
      },
    ] },
  });

    // Wallet ui
    const { data: [{ id: dependenceWalletUi }] } = await deep.insert({
      type_id: ContainId,
      from_id: packageId,
      to_id: WalletUiPackageId,
      in: { data: [
        {
          type_id: ContainId,
          from_id: packageId,
          string: { data: { value: 'dependenceWalletUi' } },
        },
      ] },
    });

    // Payment ui
    const { data: [{ id: dependencePaymentUi }] } = await deep.insert({
      type_id: ContainId,
      from_id: packageId,
      to_id: PaymentUiPackageId,
      in: { data: [
        {
          type_id: ContainId,
          from_id: packageId,
          string: { data: { value: 'dependencePaymentUi' } },
        },
      ] },
    });



  return {packageId, unitId1, walletId1, walletId2, portfolio1Id};
};