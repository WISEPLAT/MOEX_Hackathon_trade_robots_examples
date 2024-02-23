import React, { useEffect, useRef } from 'react';
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
  Badge,
  Flex,
  useColorModeValue,
  Drawer,
  DrawerBody,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
} from "@chakra-ui/react"
import { useTranslation } from 'react-i18next'


export const PaymentUi = () => {
  const { t, i18n } = useTranslation()

  const fromSrc = "";
  const toSrc = "";
  const unitSrc = "";
  const fromId = 7101;
  const toId = 7102;
  const unitId = 7103;

  const wrapperRef = useRef(null);
  const bg = useColorModeValue('#fff', '#181818');

  return (
    <Box sx={{position: 'relative'}} ref={wrapperRef}>
      <Drawer placement="bottom" onClose={()=>{}} isOpen={false} portalProps={{containerRef: wrapperRef}}>
        <DrawerOverlay />
        <DrawerContent>
          <DrawerHeader borderBottomWidth='1px'>Basic Drawer</DrawerHeader>
          <DrawerBody>
            <p>Some contents...</p>
            <p>Some contents...</p>
            <p>Some contents...</p>
          </DrawerBody>
        </DrawerContent>
      </Drawer>
      <Box maxW='sm' minW='sm' w='sm' borderWidth='1px' borderRadius='lg' overflow='hidden' p='4' bg={bg}>
        <Text fontSize='xl' fontWeight='bold' mb={4}>
          {t('Transaction')} #1234123488
        </Text>
        <Flex mb={3} alignItems='center'>
          <Flex alignItems='center'>
            <Text fontWeight='semibold' mr={1}>{t('From')}:</Text>
            <Text>#</Text>
            <Editable placeholder="" value={"10284"} isDisabled={false} mr={1}>
              <EditablePreview w={'100%'} />
              <EditableInput />
            </Editable>
          </Flex>
          { fromSrc ? (<Avatar sx={{width: '24px', height: '24px'}} ml={1} name='' src={unitSrc} mb='1'/>) : (<Box ml={1}><Identicon linkId={fromId} size={24} /></Box>)}
          <Text ml={2} sx={{whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>Кошелек кадетского фонда</Text>
        </Flex>
        <Flex mb={3} alignItems='center'>
          <Flex alignItems='center'>
            <Text fontWeight='semibold' mr={1}>{t('To')}:</Text>
            <Text>#</Text>
            <Editable placeholder="" value={"11341"} isDisabled={false} mr={1}>
              <EditablePreview w={'100%'} />
              <EditableInput />
            </Editable>
          </Flex>
          { toSrc ? (<Avatar sx={{width: '24px', height: '24px'}} ml={1} name='' src={unitSrc} mb='1'/>) : (<Box ml={1}><Identicon linkId={toId} size={24} /></Box>)}
          <Text ml={2} sx={{whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>Кошелек группы охвата</Text>
        </Flex>
        <Flex mb={3} alignItems='center'>
          <Flex alignItems='center'>
            <Text fontWeight='semibold' mr={1}>{t('Amount')}:</Text>
            <Editable placeholder="" value={"100"} isDisabled={false} mr={1}>
              <EditablePreview w={'100%'} />
              <EditableInput />
            </Editable>
            <Text>DOGE</Text>
          </Flex>
          { unitSrc ? (<Avatar sx={{width: '24px', height: '24px'}} ml={1} name='' src={unitSrc} mb='1'/>) : (<Box ml={1}><Identicon linkId={unitId} size={24} /></Box>)}
        </Flex>
        <Flex mb={3} alignItems='center' w={'100%'}>
          <Text fontWeight='semibold' mr={1}>{t('Description')}:</Text>
          <Editable placeholder="" value={"-"} isDisabled={false} mr={1} w={'100%'}>
            <EditablePreview w={'100%'} />
            <EditableInput />
          </Editable>
        </Flex>

        <Button colorScheme='blue' display='block' w='100%' size='md' variant='outline' mr={4} onClick={async () => {}}>
          {t('Send')}
        </Button>
        {/* <Badge ml='1' fontSize='1.5rem' colorScheme='orange' variant='outline'>
          Processing
        </Badge> */}
      </Box>
    </Box>
  )
};
