import { DeepClient } from "@deep-foundation/deeplinks/imports/client";
import { TypesStore } from "./typesStore";
import debug from "debug";
const log = debug("create-empty-package");

export const publishPackage = async ({deep, Types, packageName, packageId}: {
  deep: DeepClient,
  packageName: string,
  packageId: number,
  Types: TypesStore,
}) => {
  const {
    ContainId,
    PublishId,
    PackageQueryId,
  } = Types;
  console.log({ContainId, PublishId, PackageQueryId});

  // publish
  const { data: [{ id: publishId }] } = await deep.insert({
    type_id: PublishId,
    from_id: packageId,
    to: {
      type_id: PackageQueryId,
      string: { data: { value: packageName } },
    },
    in: { data: [
      {
        type_id: ContainId,
        from_id: deep.linkId,
      },
    ] },
  });
  console.log({publishId});

  return {publishId};
}