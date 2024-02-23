async ({ deep, require }) => {
  const React = require('react');
  const { useState, useEffect } = React;
  const { useColorModeValue, Box, Text, Avatar, Wrap, WrapItem, Editable, EditablePreview, EditableInput, EditableTextarea, Center, Flex, Divider, Button, Tooltip } = require('@chakra-ui/react');
  const AsyncFileId = await deep.idLocal("@deep-foundation/core", "AsyncFile");
  var UnitId = await deep.id("@suenot/unit", "Unit");
  var NameId = await deep.id("@suenot/name", "Name");
  var DescriptionId = await deep.id("@suenot/description", "Description");
  var TickerId = await deep.id("@suenot/ticker", "Ticker");
  var AvatarId = await deep.id("@suenot/avatar", "Avatar");

  const WalletId = await deep.id("@suenot/wallet", "Wallet");
  const ContainUnitId = await deep.id("@suenot/wallet", "ContainUnit");
  // const AvatarId = await deep.id("@suenot/wallet", "Avatar");
  // const DescriptionId = await deep.id("@suenot/wallet", "Description");
  // const NameId = await deep.id("@suenot/wallet", "Name");

  var PaymentId = await deep.id("@deep-foundation/payments", "Payment");
  var PaymentSumId = await deep.id("@deep-foundation/payments", "Sum");
  var PaymentPayedId = await deep.id("@deep-foundation/payments", "Payed");
  
  const bg = useColorModeValue("#fff", "#18202b");

  return ({ fillSize, style, link }) => {

    const data = deep.useDeepSubscription({
      _or: [
        // get async file for Wallet
        {
          type_id: AsyncFileId,
          to_id: link.id,
        },
        // get avatar for Wallet
        {
          type_id: AvatarId,
          to_id: link.id,
        },
        // get description for Wallet
        {
          type_id: DescriptionId,
          to_id: link.id,
        },
        // get name for Wallet
        {
          type_id: NameId,
          to_id: link.id,
        },
        // Wallet contain units
        {
          type_id: ContainUnitId,
          to: {
            type_id: UnitId,
          },
          from: {
            type_id: WalletId
          }
        },

        // get async file for Unit
        {
          type_id: AsyncFileId,
          to: {
            type_id: UnitId,
            in: {
              type_id: ContainUnitId,
              from_id: link.id
            }
          },
        },
        // get avatar for Unit
        {
          type_id: AvatarId,
          to: {
            type_id: UnitId,
            in: {
              type_id: ContainUnitId,
              from_id: link.id
            }
          },
        },
        // get ticker for Unit
        {
          type_id: TickerId,
          to: {
            type_id: UnitId,
            in: {
              type_id: ContainUnitId,
              from_id: link.id
            }
          },
        },
        // get name for Unit
        {
          type_id: NameId,
          to: {
            type_id: UnitId,
            in: {
              type_id: ContainUnitId,
              from_id: link.id
            }
          },
        },
      ]
    });

    const unitFileData = deep.minilinks.query({
      to: {
        type_id: UnitId,
        in: {
          type_id: ContainUnitId,
          from_id: link.id
        }
      },
      type_id: AsyncFileId,
    });

    const unitNameData = deep.minilinks.query({
      to: {
        type_id: UnitId,
        in: {
          type_id: ContainUnitId,
          from_id: link.id
        }
      },
      type_id: NameId,
    });
    const unitTickerData = deep.minilinks.query({
      to: {
        type_id: UnitId,
        in: {
          type_id: ContainUnitId,
          from_id: link.id
        }
      },
      type_id: TickerId,
    });
    const unitAvatarData = deep.minilinks.query({
      to: {
        type_id: UnitId,
        in: {
          type_id: ContainUnitId,
          from_id: link.id
        }
      },
      type_id: AvatarId,
    });


    const walletNameData = deep.minilinks.query({
      type_id: NameId,
      to_id: link.id,
    })

    const walletDescriptionData = deep.minilinks.query({
      type_id: DescriptionId,
      to_id: link.id,
    })

    const walletAvatarData = deep.minilinks.query({
      type_id: AvatarId,
      to_id: link.id,
    })

    const walletFileData = deep.minilinks.query({
      type_id: AsyncFileId,
      to_id: link.id,
    })


    var unitFileValue = unitFileData?.[0]?.id && `/api/file?linkId=${unitFileData?.[0]?.id}`;
    var unitAvatarValue = unitAvatarData?.[0]?.value?.value || "";
    var unitAvatarId = unitAvatarData?.[0]?.id;
    // File has more priority than avatar (url)
    var unitSrcValue = unitFileValue || unitAvatarValue || "";

    var unitNameValue = unitNameData?.[0]?.value?.value || '';
    var unitNameId = unitNameData?.[0]?.id;
    var unitTickerValue = unitTickerData?.[0]?.value?.value || "";
    var unitTickerId = unitTickerData?.[0]?.id;
    var unitSrc = unitFileValue || unitAvatarValue || "";


    var walletFileValue = walletFileData?.[0]?.id && `/api/file?linkId=${walletFileData?.[0]?.id}`;
    var walletAvatarValue = walletAvatarData?.[0]?.value?.value || "";
    var walletAvatarId = walletAvatarData?.[0]?.id;
    // File has more priority than avatar (url)
    const _walletSrcValue = walletFileValue || walletAvatarValue || "";
    // If wallet doesn't have avatar, use unit avatar
    const walletSrcValue = _walletSrcValue || unitSrcValue || "";

    var walletNameValue = walletNameData?.[0]?.value?.value || '';
    var walletNameId = walletNameData?.[0]?.id;
    var walletDescriptionValue = walletDescriptionData?.[0]?.value?.value || "";
    var walletDescriptionId = walletDescriptionData?.[0]?.id;

    const [walletName, setWalletName] = useState(walletNameValue);
    const [walletDescription, setWalletDescription] = useState(walletDescriptionValue);
    const [walletFile, setWalletFile] = useState(walletFileValue);
    const [walletAvatar, setWalletAvatar] = useState(walletAvatarValue);
    const [walletSrc, setWalletSrc] = useState(walletSrcValue);

    const amount = link?.value?.value || 0;
    const amountFixed = typeof(amount) === 'number' ? amount.toFixed(8) : "";

    return <div>
      <Box maxW='sm' minW='sm' w='sm' borderWidth='1px' borderRadius='lg' overflow='hidden' p='4' bg={bg}>
        <div>
          <Flex
            align="center"
            justify="center"
          >
            <Avatar size='2xl' name='' src={walletSrc} mb='1' />
          </Flex>
        </div>
        <Editable placeholder="Insert name" value={walletName} onChange={async (value) => {
          setWalletName(value)
        }}>
          <EditablePreview w={'100%'} />
          <EditableInput />
        </Editable>
        
          <Text>Amount: {amountFixed} {unitTickerValue} <Tooltip label={unitNameValue}><Avatar size='sm' name='' src={unitSrc} mb='1'/></Tooltip></Text>
        
        <Editable placeholder="Insert description" value={walletDescription} onChange={async (value) => {
          setWalletDescription(value)
        }}>
          <EditablePreview w={'100%'} />
          <EditableTextarea />
        </Editable>
        <Divider />
        <Editable placeholder="Insert avatar url" value={walletAvatar} onChange={async (value) => {
          setWalletAvatar(value);
          const newSrc = walletFile || value || "";
          setWalletSrc(newSrc);
        }}>
          <EditablePreview w={'100%'} />
          <EditableInput />
        </Editable>
        <Button colorScheme='teal' size='md' variant='outline' onClick={async () => {
          if (walletName === undefined) setWalletName("");
          if (walletDescription === undefined) setWalletDescription("");
          if (walletAvatar === undefined || walletAvatar === null) setWalletAvatar("");

          if (!walletNameId) {
            console.log("Wallet doesn't exist")
            const { data: [{ id: _walletNameId }] } = await deep.insert({
              type_id: NameId,
              from_id: link.id,
              to_id: link.id,
              string: { data: { value: walletName } },
            })
            walletNameId = _walletNameId;
          } else {
            console.log("Wallet exist", {walletNameId, NameId, walletName})
            const { data: [{ link: _walletNameId }] } = await deep.update(
              { link_id: walletNameId },
              { value: walletName },
              { table: 'strings', returning: `link { ${deep.selectReturning} }` }
            );
            console.log({_walletNameId});
          }

          if (!walletDescriptionId) {
            console.log("Description doesn't exist")
            const { data: [{ id: _walletDescriptionId }] } = await deep.insert({
              type_id: DescriptionId,
              from_id: link.id,
              to_id: link.id,
              string: { data: { value: walletDescription } },
            })
            walletDescriptionId = _walletDescriptionId;
          } else {
            console.log("Description exist")
            const { data: [{ link: _walletDescriptionId }] } = await deep.update(
              { link_id: walletDescriptionId },
              { value: walletDescription },
              { table: 'strings', returning: `link { ${deep.selectReturning} }` }
            );
            console.log({_walletDescriptionId});
          }

          if (!walletAvatarId) {
            const { data: [{ id: _walletAvatarId }] } = await deep.insert({
              type_id: AvatarId,
              from_id: link.id,
              to_id: link.id,
              string: { data: { value: walletAvatar } },
            })
            walletAvatarId = _walletAvatarId;
          } else {
            const { data: [{ link: _walletAvatarId }] } = await deep.update(
              { link_id: walletAvatarId },
              { value: walletAvatar },
              { table: 'strings', returning: `link { ${deep.selectReturning} }` }
            );
          }
        }}>
          Save
        </Button>
      </Box>
    </div>;
  }
}