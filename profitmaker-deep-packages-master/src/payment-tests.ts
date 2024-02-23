import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
const log = debug("portfolio");

export const createPaymentTests = async ({deep, Types, packageName, packageId}: {
  deep: DeepClient,
  packageName: string,
  Types: TypesStore,
  packageId: number,
}) => {
  const {
    ContainId,
  } = Types;

  const PaymentId = await deep.id('@deep-foundation/payments', 'Payment');
  const Pay = await deep.id('@deep-foundation/payments', 'Pay');
  const Sum = await deep.id('@deep-foundation/payments', 'Sum');
  const Payed = await deep.id('@deep-foundation/payments', 'Payed');
  const ObjectId = await deep.id('@deep-foundation/payments', 'Object');
  const Storage = await deep.id('@deep-foundation/payments', 'Storage');
  const Url = await deep.id('@deep-foundation/payments', 'Url');

  const TaskId = await deep.id('@suenot/task', 'Task');

  const PaymentsSymbolsPackageId = await deep.id('@suenot/payments-symbols');

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

  const PortfolioId = await deep.id('@suenot/portfolio', 'Portfolio');
  const ContainWalletId = await deep.id('@suenot/portfolio', 'ContainWallet');


  // console.log({packageName, packageId, UnitId, ContainId, NameId, TickerId, AvatarId, DescriptionId, WalletId, ContainUnitId, PaymentId});

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

  // Создаем unit1 name
  const { data: [{ id: unit1NameId }] } = await deep.insert({
    type_id: NameId,
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
    type_id: TickerId,
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
    type_id: AvatarId,
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
      type_id: DescriptionId,
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
      string: { data: { value: 'Dogecoin is a popular cryptocurrency that started as a playful meme in 2013. It features the Shiba Inu dog from the "Doge" internet meme as its console.logo. Despite its humorous origins, Dogecoin has gained a dedicated following and is used for tipping content creators, charitable donations, and as a digital currency for various online payments. It distinguishes itself with a vibrant and welcoming community and relatively low payment fees.' } },
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
    type_id: NameId,
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
    type_id: DescriptionId,
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
      type_id: AvatarId,
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

  // Создаем wallet3
  const { data: [{ id: walletId3 }] } = await deep.insert({
    type_id: WalletId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Кошелек Кадетского фонда' } },
      },
    ] },
    out: { data: [
      {
        type_id: ContainUnitId,
        to_id: unitId1,
      }
    ] },
    number: { data: { value: 0 } },
  });
  console.log({walletId3});

  // Создаем wallet3
  const { data: [{ id: walletId4 }] } = await deep.insert({
    type_id: WalletId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Кошелек Группы Охвата' } },
      },
    ] },
    out: { data: [
      {
        type_id: ContainUnitId,
        to_id: unitId1,
      }
    ] },
    number: { data: { value: 0 } },
  });
  console.log({walletId4});

  // Создаем task1
  const { data: [{ id: task1Id }] } = await deep.insert({
    type_id: TaskId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Создание MVP deep.memo' } },
      },
    ] },
    out: { data: [
    ] },
  });
  console.log({task1Id});

  // Создаем payment1
  const { data: [{ id: paymentId1 }] } = await deep.insert({
    type_id: PaymentId,
    from_id: walletId1,
    to_id: walletId2,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'paymentId1' } },
      },
    ] },
    out: { data: [
      {
        type_id: ObjectId,
        to_id: task1Id,
      }
    ] },
    // number: { data: { value: 222.00000001 } },
  });
  console.log({paymentId1});

  // Создаем payment1 sum
  const { data: [{ id: payment1SumId }] } = await deep.insert({
    type_id: Sum,
    from_id: paymentId1,
    to_id: paymentId1,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'payment1Sum' } },
      },
    ] },
    number: { data: { value: 222.00000001 } },
  });

  // Unit ui
  const { data: [{ id: dependenceUnitUi }] } = await deep.insert({
    type_id: ContainId,
    from_id: packageId,
    to_id: UnitUiPackageId,
    string: { data: { value: 'dependenceUnitUi' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'containDependenceUnitUi' } },
      },
    ] },
  });

  // Wallet ui
  const { data: [{ id: dependenceWalletUi }] } = await deep.insert({
    type_id: ContainId,
    from_id: packageId,
    to_id: WalletUiPackageId,
    string: { data: { value: 'dependenceWalletUi' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'containDependenceWalletUi' } },
      },
    ] },
  });

  // Payment ui
  const { data: [{ id: dependencePaymentUi }] } = await deep.insert({
    type_id: ContainId,
    from_id: packageId,
    to_id: PaymentUiPackageId,
    string: { data: { value: 'dependencePaymentUi' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'containDependencePaymentUi' } },
      },
    ] },
  });

  // Payments symbols
  const { data: [{ id: dependencePaymentsSymbols }] } = await deep.insert({
    type_id: ContainId,
    from_id: packageId,
    to_id: PaymentsSymbolsPackageId,
    string: { data: { value: 'dependencePaymentsSymbols' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'containDependencePaymentsSymbols' } },
      },
    ] },
  });

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

      // Создаем emission1
  const { data: [{ id: emissionId1 }] } = await deep.insert({
    type_id: PaymentId,
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

    // Создаем emission1 sum
    const { data: [{ id: emission1SumId }] } = await deep.insert({
      type_id: Sum,
      from_id: emissionId1,
      to_id: emissionId1,
      in: { data: [
        {
          type_id: ContainId,
          from_id: packageId,
          string: { data: { value: 'emission1Sum' } },
        },
      ] },
      number: { data: { value: 999.99 } },
    });

  return {packageId, unitId1, walletId1, walletId2, paymentId1, payment1SumId, PaymentId, Pay, Sum, Payed, ObjectId, Storage, Url, UnitId, NameId, TickerId, AvatarId, DescriptionId, WalletId, ContainUnitId, UnitUiPackageId, WalletUiPackageId, PaymentUiPackageId, PaymentsSymbolsPackageId, dependenceUnitUi, dependenceWalletUi, dependencePaymentUi, dependencePaymentsSymbols};
};