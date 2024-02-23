import _ from 'lodash';
import 'dotenv/config';

import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { generateApolloClient } from "@deep-foundation/hasura/client";

const apolloClient = generateApolloClient({
  path: process.env.PUBLIC_GQL_PATH,
  ssl: Boolean(process.env.PUBLIC_GQL_SSL),
  token: process.env.PRIVATE_GQL_TOKEN,
});
const unloginedDeep = new DeepClient({ apolloClient });
const guest = await unloginedDeep.guest();
const guestDeep = new DeepClient({ deep: unloginedDeep, ...guest });
const admin = await guestDeep.login({
  linkId: await guestDeep.id('deep', 'admin'),
});
const deep = new DeepClient({ deep: guestDeep, ...admin });



const delay = (time = 1000) => new Promise(res => setTimeout(res, time));

const f = async () => {
  // const guest = await unloginedDeep.guest();
  // const guestDeep = new DeepClient({ deep: unloginedDeep, ...guest });
  // const admin = await guestDeep.login({ linkId: await guestDeep.id('deep', 'admin') });
  // const deep = new DeepClient({ deep: guestDeep, ...admin });

  const User = await deep.id('@deep-foundation/core', 'User');
  const Type = await deep.id('@deep-foundation/core', 'Type');
  const Any = await deep.id('@deep-foundation/core', 'Any');
  const Join = await deep.id('@deep-foundation/core', 'Join');
  const Contain = await deep.id('@deep-foundation/core', 'Contain');
  const Value = await deep.id('@deep-foundation/core', 'Value');
  const String = await deep.id('@deep-foundation/core', 'String');
  const Package = await deep.id('@deep-foundation/core', 'Package');

  const SyncTextFile = await deep.id('@deep-foundation/core', 'SyncTextFile');
  const dockerSupportsJs = await deep.id('@deep-foundation/core', 'dockerSupportsJs');
  const Handler = await deep.id('@deep-foundation/core', 'Handler');
  const HandleInsert = await deep.id('@deep-foundation/core', 'HandleInsert');
  const HandleDelete = await deep.id('@deep-foundation/core', 'HandleDelete');

  const Tree = await deep.id('@deep-foundation/core', 'Tree');
  const TreeIncludeNode = await deep.id('@deep-foundation/core', 'TreeIncludeNode');
  const TreeIncludeUp = await deep.id('@deep-foundation/core', 'TreeIncludeUp');
  const TreeIncludeFromCurrent = await deep.id('@deep-foundation/core', 'TreeIncludeFromCurrent');

  const Rule = await deep.id('@deep-foundation/core', 'Rule');
  const RuleSubject = await deep.id('@deep-foundation/core', 'RuleSubject');
  const RuleObject = await deep.id('@deep-foundation/core', 'RuleObject');
  const RuleAction = await deep.id('@deep-foundation/core', 'RuleAction');
  const Selector = await deep.id('@deep-foundation/core', 'Selector');
  const SelectorInclude = await deep.id('@deep-foundation/core', 'SelectorInclude');
  const SelectorExclude = await deep.id('@deep-foundation/core', 'SelectorExclude');
  const SelectorTree = await deep.id('@deep-foundation/core', 'SelectorTree');
  const containTree = await deep.id('@deep-foundation/core', 'containTree');
  const AllowInsertType = await deep.id('@deep-foundation/core', 'AllowInsertType');
  const AllowDeleteType = await deep.id('@deep-foundation/core', 'AllowDeleteType');
  const SelectorFilter = await deep.id('@deep-foundation/core', 'SelectorFilter');
  const Query = await deep.id('@deep-foundation/core', 'Query');
  const usersId = await deep.id('deep', 'users');

  const { data: [{ id: packageId }] } = await deep.insert({
  // const data = await deep.insert({
    type_id: Package,
    string: { data: { value: `@deep-foundation/profitmaker` } },
    in: { data: [
      {
        type_id: Contain,
        from_id: deep.linkId,
      },
    ] },
    out: { data: [
      {
        type_id: Join,
        to_id: await deep.id('deep', 'users', 'packages'),
      },
      {
        type_id: Join,
        to_id: await deep.id('deep', 'admin'),
      },
    ] },
  });
  console.log({ packageId });

  // // INVEST PROVIDER
  // const { data: [{ id: BrokerProvider }] } = await deep.insert({
  //   type_id: Type,
  //   from_id: Any,
  //   to_id: Any,
  //   in: { data: {
  //     type_id: Contain,
  //     from_id: packageId,
  //     string: { data: { value: 'BrokerProvider' } },
  //   } },
  // });
  // console.log({ BrokerProvider });

  // // ASSET
  // const { data: [{ id: Asset }] } = await deep.insert({
  //   type_id: Type,
  //   from_id: Any,
  //   to_id: Any,
  //   in: { data: {
  //     type_id: Contain,
  //     from_id: packageId,
  //     string: { data: { value: 'Asset' } },
  //   } },
  // });
  // console.log({ Asset });

  // const { data: [{ id: Isin }] } = await deep.insert({
  //   type_id: Type,
  //   from_id: BrokerProvider,
  //   to_id: Asset,
  //   in: { data: {
  //     type_id: Contain,
  //     from_id: packageId,
  //     string: { data: { value: 'Isin' } },
  //   } },
  // });
  // console.log({ Isin });

  // const { data: [{ id: AssetTicker }] } = await deep.insert({
  //   type_id: Type,
  //   from_id: BrokerProvider,
  //   to_id: Asset,
  //   in: { data: {
  //     type_id: Contain,
  //     from_id: packageId,
  //     string: { data: { value: 'AssetTicker' } },
  //   } },
  // });
  // console.log({ AssetTicker });

  // const { data: [{ id: AssetData }] } = await deep.insert({
  //   type_id: Type,
  //   from_id: BrokerProvider,
  //   to_id: Asset,
  //   in: { data: {
  //     type_id: Contain,
  //     from_id: packageId,
  //     string: { data: { value: 'AssetData' } },
  //   } },
  // });
  // console.log({ AssetData });

  // // INSTRUMENT
  // const { data: [{ id: Instrument }] } = await deep.insert({
  //   type_id: Type,
  //   from_id: Any,
  //   to_id: Any,
  //   in: { data: {
  //     type_id: Contain,
  //     from_id: packageId,
  //     string: { data: { value: 'Instrument' } },
  //   } },
  // });
  // console.log({ Instrument });

  // const { data: [{ id: Figi }] } = await deep.insert({
  //   type_id: Type,
  //   from_id: BrokerProvider,
  //   to_id: Instrument,
  //   in: { data: {
  //     type_id: Contain,
  //     from_id: packageId,
  //     string: { data: { value: 'Figi' } },
  //   } },
  // });
  // console.log({ Figi });

  // const { data: [{ id: InstrumentTicker }] } = await deep.insert({
  //   type_id: Type,
  //   from_id: BrokerProvider,
  //   to_id: Asset,
  //   in: { data: {
  //     type_id: Contain,
  //     from_id: packageId,
  //     string: { data: { value: 'InstrumentTicker' } },
  //   } },
  // });
  // console.log({ InstrumentTicker });

  // const { data: [{ id: InstrumentData }] } = await deep.insert({
  //   type_id: Type,
  //   from_id: BrokerProvider,
  //   to_id: Instrument,
  //   in: { data: {
  //     type_id: Contain,
  //     from_id: packageId,
  //     string: { data: { value: 'InstrumentData' } },
  //   } },
  // });
  // console.log({ InstrumentData });

  // // WALLET
  // const { data: [{ id: Wallet }] } = await deep.insert({
  //   type_id: Type,
  //   from_id: User,
  //   to_id: BrokerProvider,
  //   in: { data: {
  //     type_id: Contain,
  //     from_id: packageId,
  //     string: { data: { value: 'Wallet' } },
  //   } },
  // });
  // console.log({ Wallet });

  // // TRANSACTION
  // const { data: [{ id: Transaction }] } = await deep.insert({
  //   type_id: Type,
  //   from_id: Wallet,
  //   to_id: Wallet,
  //   in: { data: {
  //     type_id: Contain,
  //     from_id: packageId,
  //     string: { data: { value: 'Transaction' } },
  //   } },
  // });
  // console.log({ Transaction });

  // const { data: [{ id: Base }] } = await deep.insert({
  //   type_id: Type,
  //   from_id: Any, // Transaction
  //   to_id: Any, // Asset
  //   in: { data: {
  //     type_id: Contain,
  //     from_id: packageId,
  //     string: { data: { value: 'Base' } },
  //   } },
  // });
  // console.log({ Base });

  // const { data: [{ id: Quote }] } = await deep.insert({
  //   type_id: Type,
  //   from_id: Any, // Transaction
  //   to_id: Any, // Asset
  //   in: { data: {
  //     type_id: Contain,
  //     from_id: packageId,
  //     string: { data: { value: 'Quote' } },
  //   } },
  // });
  // console.log({ Quote });

  // // TRANSACTION: PRICE, AMOUNT, TOTAL
  // const { data: [{ id: Price }] } = await deep.insert({
  //   type_id: Type,
  //   from_id: Transaction,
  //   to_id: Instrument,
  //   in: { data: {
  //     type_id: Contain,
  //     from_id: packageId,
  //     string: { data: { value: 'Price' } },
  //   } },
  // });
  // console.log({ Price });

  // const { data: [{ id: Amount }] } = await deep.insert({
  //   type_id: Type,
  //   from_id: Transaction,
  //   to_id: Instrument,
  //   in: { data: {
  //     type_id: Contain,
  //     from_id: packageId,
  //     string: { data: { value: 'Amount' } },
  //   } },
  // });
  // console.log({ Amount });

  // const { data: [{ id: Total }] } = await deep.insert({
  //   type_id: Type,
  //   from_id: Amount,
  //   to_id: Price,
  //   in: { data: {
  //     type_id: Contain,
  //     from_id: packageId,
  //     string: { data: { value: 'Total' } },
  //   } },
  // });
  // console.log({ Total });

};
f();
