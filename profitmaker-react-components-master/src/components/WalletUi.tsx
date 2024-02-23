import * as React from "react"
import { useState, useEffect } from 'react';
import Identicon from "./Identicon";

import {
  Box,
  Text,
  VStack,
  HStack,
  theme,
  Button,
  Editable,
  EditableInput,
  EditablePreview,
  Avatar,
  AvatarBadge,
  AvatarGroup,
  Wrap,
  WrapItem,
  AvatarProps,
  AvatarBadgeProps,
  EditableTextarea,
  Divider,
  Flex,
  Tooltip,
  useColorModeValue
} from "@chakra-ui/react"

export const WalletUi = () => {
  const unitNameValue = "Dogecoin";
  const unitTickerValue = "DOGE";
  const unitSrc = "";
  const unitDescriptionValue = 'Dogecoin is a popular cryptocurrency that started as a playful meme in 2013. It features the Shiba Inu dog from the "Doge" internet meme as its console.logo. Despite its humorous origins, Dogecoin has gained a dedicated following and is used for tipping content creators, charitable donations, and as a digital currency for various online payments. It distinguishes itself with a vibrant and welcoming community and relatively low payment fees.';
  // const svgString = identicon.generateSync({ id: 'ajido', size: 40 });

  const [walletName, setWalletName] = useState("");
  const [walletDescription, setWalletDescription] = useState(unitDescriptionValue);
  const [walletFile, setWalletFile] = useState("");
  const [walletAvatar, setWalletAvatar] = useState("");
  const [walletSrc, setWalletSrc] = useState("");
  const walletId = 7002;
  const unitId = 7003

  // setWalletSrc(svgString);

  const amount = 0;
  const amountFixed = typeof(amount) === 'number' ? amount.toFixed(8) : "";

  const bg = useColorModeValue('#fff', '#181818');
  return (
    <Box maxW='sm' minW='sm' w='sm' borderWidth='1px' borderRadius='lg' overflow='hidden' p='4' bg={bg}>
    <div>
      <Flex
        align="center"
        justify="center"
      >
        {walletSrc ? (<Avatar size='2xl' name='' src={walletSrc} mb='1' />) : (<Identicon linkId={walletId} size={128} />)}
      </Flex>
    </div>
    <Editable placeholder="Insert name" value={walletName} onChange={async (value) => {
      setWalletName(value)
    }}>
      <EditablePreview w={'100%'} />
      <EditableInput />
    </Editable>
    <Text sx={{display: 'flex', alignItems: 'center'}}>
      <Box>Amount: {amountFixed} {unitTickerValue}</Box>
      <Tooltip label={unitNameValue}>
        { unitSrc ? (<Avatar sx={{width: '24px', height: '24px'}} ml={1} name='' src={unitSrc} mb='1'/>) : (<Box ml={1}><Identicon linkId={unitId} size={24} /></Box>)}
      </Tooltip>
    </Text>
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
    <Button colorScheme='teal' size='md' variant='outline' onClick={async () => {}}>
      Save
    </Button>
  </Box>
)}
