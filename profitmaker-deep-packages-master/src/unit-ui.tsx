async ({ deep, require }) => {
  const React = require('react');
  const { useState, useEffect } = React;
  const { useColorModeValue, Box, Text, Avatar, Wrap, WrapItem, Editable, EditablePreview, EditableInput, EditableTextarea, Center, Flex, Divider, Button } = require('@chakra-ui/react');
  const AsyncFileId = await deep.idLocal("@deep-foundation/core", "AsyncFile");
  var NameId = await deep.id("@suenot/name", "Name");
  var DescriptionId = await deep.id("@suenot/description", "Description");
  var TickerId = await deep.id("@suenot/ticker", "Ticker");
  var AvatarId = await deep.id("@suenot/avatar", "Avatar");

  const bg = useColorModeValue("#fff", "#18202b");

  return ({ fillSize, style, link }) => {

    const data = deep.useDeepSubscription({
        _or: [
          {
            to_id: link.id,
            type_id: AsyncFileId,
          },
          {
            to_id: link.id,
            type_id: NameId,
          },
          {
            to_id: link.id,
            type_id: DescriptionId,
          },
          {
            to_id: link.id,
            type_id: TickerId,
          },
          {
            to_id: link.id,
            type_id: AvatarId,
          }
        ]
      }
    );
    const fileData = deep.minilinks.query({
      to_id: link.id,
      type_id: AsyncFileId
    });
    const nameData = deep.minilinks.query({
      to_id: link.id,
      type_id: NameId
    });
    const unitDescriptionData = deep.minilinks.query({
      to_id: link.id,
      type_id: DescriptionId
    });
    const tickerData = deep.minilinks.query({
      to_id: link.id,
      type_id: TickerId
    });
    const avatarData = deep.minilinks.query({
      to_id: link.id,
      type_id: AvatarId
    });



    var unitFileValue = fileData?.[0]?.id && `/api/file?linkId=${fileData?.[0]?.id}`;
    var unitAvatarValue = avatarData?.[0]?.value?.value || "";
    var unitAvatarId = avatarData?.[0]?.id;
    // File has more priority than avatar (url)
    var unitSrcValue = unitFileValue || unitAvatarValue || "";

    var unitNameValue = nameData?.[0]?.value?.value || '';
    var unitNameId = nameData?.[0]?.id;
    var unitTickerValue = tickerData?.[0]?.value?.value || '';
    var unitTickerId = tickerData?.[0]?.id;
    var unitDescriptionValue = unitDescriptionData?.[0]?.value?.value || "";
    var unitDescriptionId = unitDescriptionData?.[0]?.id;
    console.log({data});

    const [unitName, setUnitName] = useState(unitNameValue);
    const [unitTicker, setUnitTicker] = useState(unitTickerValue);
    const [unitDescription, setUnitDescription] = useState(unitDescriptionValue);
    const [unitFile, setUnitFile] = useState(unitFileValue);
    const [unitAvatar, setUnitAvatar] = useState(unitAvatarValue);
    const [unitSrc, setUnitSrc] = useState(unitSrcValue);

    return <div>
      <Box maxW='sm' minW='sm' w='sm' borderWidth='1px' borderRadius='lg' overflow='hidden' p='4' bg={bg}>
        <div>
          <Flex
            align="center"
            justify="center"
          >
            <Avatar size='2xl' name='' src={unitSrc} mb='1' />
          </Flex>
        </div>
        <Editable placeholder="Insert name" value={unitName} onChange={async (value) => {
          setUnitName(value)
        }}>
          <EditablePreview w={'100%'} />
          <EditableInput />
        </Editable>
        <Editable placeholder="Insert ticker" value={unitTicker} onChange={async (value) => {
          setUnitTicker(value)
        }}>
          <EditablePreview w={'100%'} />
          <EditableInput />
        </Editable>
        <Editable placeholder="Insert description" value={unitDescription} onChange={async (value) => {
          setUnitDescription(value)
        }}>
          <EditablePreview w={'100%'} />
          <EditableTextarea />
        </Editable>
        <Divider />
        <Editable placeholder="Insert avatar url" value={unitAvatar} onChange={async (value) => {
          setUnitAvatar(value);
          const newSrc = unitFile || value || "";
          setUnitSrc(newSrc);
        }}>
          <EditablePreview w={'100%'} />
          <EditableInput />
        </Editable>
        <Button colorScheme='teal' size='md' variant='outline' onClick={async () => {
          if (unitName === undefined) setUnitName("");
          if (unitDescription === undefined) setUnitDescription("");
          if (unitTicker === undefined) setUnitTicker("");
          if (unitAvatar === undefined || unitAvatar === null) setUnitAvatar("");

          if (!unitNameId) {
            console.log("Unit doesn't exist")
            const { data: [{ id: _unitNameId }] } = await deep.insert({
              type_id: NameId,
              from_id: link.id,
              to_id: link.id,
              string: { data: { value: unitName } },
            })
            unitNameId = _unitNameId;
          } else {
            console.log("Unit exist", {unitNameId, NameId, unitName})
            const { data: [{ link: _unitNameId }] } = await deep.update(
              { link_id: unitNameId },
              { value: unitName },
              { table: 'strings', returning: `link { ${deep.selectReturning} }` }
            );
            console.log({_unitNameId});
          }

          if (!unitDescriptionId) {
            console.log("Description doesn't exist")
            const { data: [{ id: _unitDescriptionId }] } = await deep.insert({
              type_id: DescriptionId,
              from_id: link.id,
              to_id: link.id,
              string: { data: { value: unitDescription } },
            })
            unitDescriptionId = _unitDescriptionId;
          } else {
            console.log("Description exist")
            const { data: [{ link: _unitDescriptionId }] } = await deep.update(
              { link_id: unitDescriptionId },
              { value: unitDescription },
              { table: 'strings', returning: `link { ${deep.selectReturning} }` }
            );
            console.log({_unitDescriptionId});
          }

          if (!unitTickerId) {
            const { data: [{ id: _unitTickerId }] } = await deep.insert({
              type_id: TickerId,
              from_id: link.id,
              to_id: link.id,
              string: { data: { value: unitTicker } },
            })
            unitTickerId = _unitTickerId;
          } else {
            const { data: [{ link: _unitTickerId }] } = await deep.update(
              { link_id: unitTickerId },
              { value: unitTicker },
              { table: 'strings', returning: `link { ${deep.selectReturning} }` }
            );
          }

          if (!unitAvatarId) {
            const { data: [{ id: _unitAvatarId }] } = await deep.insert({
              type_id: AvatarId,
              from_id: link.id,
              to_id: link.id,
              string: { data: { value: unitAvatar } },
            })
            unitAvatarId = _unitAvatarId;
          } else {
            const { data: [{ link: _unitAvatarId }] } = await deep.update(
              { link_id: unitAvatarId },
              { value: unitAvatar },
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