import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import debug from "debug";
const log = debug("remove-package");

export const removePackage =  async ({deep, packageName}: {deep: DeepClient, packageName: string}) => {
  console.log('removePackage', {packageName});
  var packageId: number | undefined = undefined;
  var packageNamespaceId: number | undefined = undefined;
  var deletedLinks: any[] = [];
  const PackageNamespaceId = await deep.id('@deep-foundation/core', 'PackageNamespace');
  const PackageQueryId = await deep.id('@deep-foundation/core', 'PackageQuery');
  const PublishId = await deep.id('@deep-foundation/npm-packager', 'Publish');
  const ContainId = await deep.id('@deep-foundation/core', 'Contain');
  const containTreeId = await deep.id('@deep-foundation/core', 'containTree');
  log({PackageNamespaceId, ContainId, containTreeId});

  try {
    packageId = await deep.id(packageName);
  } catch (error) {}
  console.log({packageName, packageId});

  // Contain to Publish
  try {
    const { data: publishContains } = await deep.select({
      type_id: ContainId,
      to: {
        type_id: PublishId
      },
      // from_id: deep.linkId;
    });
    log({publishContains});

    const publishContainIds = publishContains.map((link) => link.id);
    log({publishContainIds});

    for (const publishContainId of publishContainIds) {
      const resultDelete = await deep.delete({
        id: publishContainId
      });
      log({resultDelete})
      deletedLinks = [...deletedLinks, ...resultDelete?.data]
    }
  } catch (error) {}

  // Publish
  try {
    const { data: publishPackageQueries } = await deep.select({
      type_id: PublishId,
    });
    log({publishPackageQueries});

    const publishPackageQueriesIds = publishPackageQueries.map((link) => link.id);
    log({publishPackageQueriesIds});

    for (const publishPackageQueryId of publishPackageQueriesIds) {
      const resultDelete = await deep.delete({
        id: publishPackageQueryId
      });
      log({resultDelete})
      deletedLinks = [...deletedLinks, ...resultDelete?.data]
    }
  } catch (error) {}

  // try {
  //   const { data: publishLinks } = await deep.select({
  //     type_id: ContainId,
  //     to: {
  //       type_id: PublishId,
  //     },
  //   });
  //   log({publishLinks});

  //   const publishIds = publishLinks.map((link) => link.id);
  //   log({publishIds});

  //   for (const publishId of publishIds) {
  //     const resultDelete = await deep.delete({
  //       id: publishId
  //     });
  //     log({resultDelete})
  //     deletedLinks = [...deletedLinks, ...resultDelete?.data]
  //   }
  // } catch (error) {}

  try {
    const { data: packageNamespaceLinks } = await deep.select({
      type_id: PackageNamespaceId,
      value: packageName,
    });
    log({packageId, packageNamespaceLinks});

    const packageNamespaceIds = packageNamespaceLinks.map((link) => link.id);
    console.log({packageNamespaceIds});

    for (const packageNamespaceId of packageNamespaceIds) {
      const resultDelete = await deep.delete({
        type_id: ContainId,
        to_id: packageNamespaceId,
      });
      log({resultDelete})
      deletedLinks = [...deletedLinks, ...resultDelete?.data]
    }

    for (const packageNamespaceId of packageNamespaceIds) {
      const resultDelete = await deep.delete({
        id: packageNamespaceId,
      });
      log({resultDelete})
      deletedLinks = [...deletedLinks, ...resultDelete?.data]
    }

  } catch (error) {}

  try {
    const { data: [{ id: containerLinkId }] } = await deep.select({
      to_id: packageId,
      type_id: ContainId,
    });
    log({packageId, containerLinkId});
    const resultDelete = await deep.delete({
      up: {
        tree_id: containTreeId,
        parent: {
          type_id: ContainId,
          to_id: packageId,
        },
      },
    });
    log({resultDelete})
    deletedLinks = [...deletedLinks, ...resultDelete?.data]
    log({deletedLinks})
  } catch (error) {
    packageId = undefined;
  }
  try {
    packageId = await deep.id(packageName);
  } catch (error) {}
  return deletedLinks;
}