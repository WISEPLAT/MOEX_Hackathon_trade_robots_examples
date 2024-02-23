import _ from 'lodash';
import 'dotenv/config';
import latestVersion from 'latest-version';
import { incrementPatchVersion } from './incrementPatchVersion';

import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { generateApolloClient } from "@deep-foundation/hasura/client";
// import { createProfitmaker } from "./profitmaker";
import { createUnit } from "./unit";
import { createUnitUi }from "./unit-ui";
// import { createUnitUiEn } from './unit-ui-en';
// import { createUnitUiRu } from './unit-ui-ru';
import { createWallet } from "./wallet";
import { createWalletUi } from "./wallet-ui";
import { createPortfolio } from './portfolio';
import { createPortfolioUi } from './portfolio-ui';
// import { createTransaction } from './transaction';
// import { createTransactionUi } from './transaction-ui';
// import { createEmission } from './emission';
// import { createEmissionUi } from './emission-ui';
// import { createTransactionTests } from './transaction-tests';
// import { createEmissionTests } from './emission-tests';
import { createPortfolioTests } from './portfolio-tests';
import { createPair } from './pair';
import { createExchange } from './exchange';
import { createInstrument } from './instrument';
import { createLanguage } from './language';
import { createLocale } from './locale';
import { createTask } from './task';
import { createName } from './name';
import { createDescription } from './description';
import { createTicker } from './ticker';
import { createAvatar } from './avatar';
import { createPaymentUi } from './payment-ui';
import { createPaymentTests } from './payment-tests';
import { createPaymentsSymbols } from './payments-symbols';
import { createAvatarEditUi } from './avatar-edit-ui';
import { createLocaleEditUi } from './locale-edit-ui';
import { createPaymentProvider } from './payment-provider';

import { removePackage } from "./removePackage";
import { createEmptyPackage } from './createEmptyPackage';
import { publishPackage } from './publishPackage';
import { TypesStore, createTypesStore } from "./typesStore";

import debug from "debug";
import { sleep } from './sleep';
const log = debug("deep");

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
export const deep = new DeepClient({ deep: guestDeep, ...admin });

const f = async () => {
  log('initStore');
  const Types: any = await createTypesStore({deep});
  log('end initStore');

  const packages: any[] = [
    {
      name: '@suenot/task',
      versionUpdate: true,
      upload: true,
      createFn: createTask,
      path: './task',
    },
    {
      name: '@suenot/payments-symbols',
      versionUpdate: true,
      upload: true,
      createFn: createPaymentsSymbols,
      path: './payments-symbols',
    },
    {
      name: '@suenot/name',
      versionUpdate: true,
      upload: true,
      createFn: createName,
      path: './name',
    },
    {
      name: '@suenot/description',
      versionUpdate: true,
      upload: true,
      createFn: createDescription,
      path: './description',
    },
    {
      name: '@suenot/ticker',
      versionUpdate: true,
      upload: true,
      createFn: createTicker,
      path: './name',
    },
    {
      name: '@suenot/avatar',
      versionUpdate: true,
      upload: true,
      createFn: createAvatar,
      path: './avatar',
    },
    {
      name: '@suenot/unit',
      versionUpdate: true,
      upload: true,
      createFn: createUnit,
      path: './unit',
    },
    {
      name: '@suenot/wallet',
      versionUpdate: true,
      upload: true,
      createFn: createWallet,
      path: './wallet',
      delay: 10000,
    },
    {
      name: '@suenot/unit-ui',
      versionUpdate: true,
      upload: true,
      createFn: createUnitUi,
      path: './unit-ui',
    },
    {
      name: '@suenot/wallet-ui',
      versionUpdate: true,
      upload: true,
      createFn: createWalletUi,
      path: './wallet-ui',
      delay: 10000,
    },
    {
      name: '@suenot/payment-ui',
      versionUpdate: true,
      upload: true,
      createFn: createPaymentUi,
      path: './payment-ui',
    },
    {
      name: '@suenot/payment-provider',
      versionUpdate: true,
      upload: true,
      createFn: createPaymentProvider,
      path: './payment-provider',
    },
    // {
    //   name: '@suenot/profitmaker',
    //   versionUpdate: true,
    //   upload: true,
    //   createFn: createProfitmaker,
    //   path: './profitmaker',
    // },
    // {
    //   name: '@suenot/language',
    //   versionUpdate: true,
    //   upload: true,
    //   createFn: createLanguage,
    //   path: './language',
    // },
    // {
    //   name: '@suenot/locale',
    //   versionUpdate: true,
    //   upload: true,
    //   createFn: createLocale,
    //   path: './locale',
    // },
    {
      name: '@suenot/portfolio',
      versionUpdate: true,
      upload: true,
      createFn: createPortfolio,
      path: './portfolio',
    },
    {
      name: '@suenot/portfolio-ui',
      versionUpdate: true,
      upload: true,
      createFn: createPortfolioUi,
      path: './portfolio-ui',
    },
    // {
    //   name: '@suenot/portfolio-tests',
    //   versionUpdate: true,
    //   upload: true,
    //   createFn: createPortfolioTests,
    //   path: './portfolio-tests',
    // },
    {
      name: '@suenot/payment-tests',
      versionUpdate: true,
      upload: true,
      createFn: createPaymentTests,
      path: './payment-tests',
      delay: 10000,
    },
    // {
    //   name: '@suenot/pair',
    //   versionUpdate: true,
    //   upload: true,
    //   createFn: createPair,
    //   path: './pair',
    // },
    // {
    //   name: '@suenot/exchange',
    //   versionUpdate: true,
    //   upload: true,
    //   createFn: createExchange,
    //   path: './exchange',
    // },
    // {
    //   name: '@suenot/instrument',
    //   versionUpdate: true,
    //   upload: true,
    //   createFn: createInstrument,
    //   path: './instrument',
    // },
    // где-то здесь ошибка (так как идет связь от пакета до synctextfile)
    // {
    //   name: '@suenot/unit-ui-ru',
    //   versionUpdate: true,
    //   upload: true,
    //   createFn: createUnitUiRu,
    //   path: './unit-ui-ru',
    // },
    // {
    //   name: '@suenot/unit-ui-en',
    //   versionUpdate: true,
    //   upload: true,
    //   createFn: createUnitUiEn,
    //   path: './unit-ui-en',
    // },
  ]

  for (const deepPackage of packages) {
    // remove old package
    const resultRemovePackage = await removePackage({ deep, packageName: deepPackage.name });
    log({deepPackage, resultRemovePackage})
  }

  for (const deepPackage of packages) {
    if (deepPackage.delay) {
      await sleep(deepPackage.delay);
    }
    // // insert new package
    const packageName = deepPackage.name;
    var lastPackageVersion = '0.0.1';
    try {
      lastPackageVersion = await latestVersion(packageName);
    } catch (error) {}
    log('Generating package version #️⃣');
    const packageVersion = deepPackage.versionUpdate ? incrementPatchVersion(lastPackageVersion) : lastPackageVersion;
    log(`Package ${packageName} version is #️⃣${packageVersion}`);
    log('Generating package 📦 and namespace 🎁');
    const {packageId, packageNamespaceId} = await createEmptyPackage({deep, Types, packageName, packageVersion});
    log(packageId, packageNamespaceId);
    // TODO: если успешно, то создавай типы для пакета
    log('Creating package types ⭐', {packageName, packageId, packageNamespaceId})
    await deepPackage.createFn({deep, Types, packageName, packageId});
    // TODO: если успешно, то публикуй пакет
    log('Publishing package 🚀', {packageName, packageId});
    if (deepPackage.versionUpdate) {
      const {publishId} = await publishPackage({deep, Types, packageName, packageId});
      log({publishId});
    }
  }
}
f();