import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
const log = debug("portfolio");

export const createPortfolio = async ({deep, Types, packageName, packageId}: {
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
    NumberId,
  } = Types;
  console.log({packageName, ContainId, SymbolId, TypeId, StringId, ValueId, NumberId});

  const WalletId = await deep.id('@suenot/wallet', 'Wallet');

  // Portfolio
  const { data: [{ id: PortfolioId }] } = await deep.insert({
    type_id: TypeId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'Portfolio' } },
      },
    ] },
    out: { data: [
    ] },
  });
  log({PortfolioId});

  // SymbolId (петличка от Portfolio к Portfolio)
  const { data: [{ id: symbolId }] } = await deep.insert({
    type_id: SymbolId,
    string: { data: { value: '💼' } },
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'symbol' } },
      },
    ] },
    from_id: PortfolioId,
    to_id: PortfolioId,
  });
  log({symbolId});

  // ContainWallet
  const { data: [{ id: ContainWalletId }] } = await deep.insert({
    type_id: TypeId,
    in: { data: [
      {
        type_id: ContainId,
        from_id: packageId,
        string: { data: { value: 'ContainWallet' } },
      },
    ] },
    from_id: PortfolioId,
    to_id: WalletId,
  });
  log({ContainWalletId});

  return {packageId, PortfolioId, symbolId, ContainWalletId};
};