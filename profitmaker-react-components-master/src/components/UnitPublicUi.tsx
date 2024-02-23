import * as React from "react"
import { useState, useEffect } from 'react';
import Identicon from "./Identicon";
import { MdBuild } from "react-icons/md";
import { UnitOptions } from "./types";
import { useTranslation } from 'react-i18next'

import {
  Box,
  Text,
  Button,
  Avatar,
  Flex,
  useColorModeValue
} from "@chakra-ui/react"

export const UnitPublicUi = ({
  onClickEditButton,
  options,
}: {
  onClickEditButton: () => void;
  options: UnitOptions,
}) => {

  const bg = useColorModeValue('#fff', '#181818');
  // const bg = useColorModeValue('#fff', '#141214');
  const { t, i18n } = useTranslation()

  return (
    <Box maxW='sm' minW='sm' w='sm' borderWidth='1px' borderRadius='lg' overflow='hidden' p='4' sx={{position: 'relative'}} bg={bg}>
      <Button leftIcon={<MdBuild />} colorScheme='pink' variant='outline' sx={{position: 'absolute', top: 4, right: 4}} onClick={onClickEditButton}>
        {t('Edit')}
      </Button>
      <div>
        <Flex
          align="center"
          justify="center"
        >
          {options.unitSrc ? (<Avatar size='2xl' name='' src={options.unitSrc} mb='1' />) : (<Identicon linkId={options.unitId} size={128} />)}
        </Flex>
      </div>
      <Flex>
        <Text fontWeight='semibold' mr={1}>{t('Name')}:</Text>
        <Text>{options.unitName}</Text>
      </Flex>
      <Flex>
        <Text fontWeight='semibold' mr={1}>{t('Ticker')}:</Text>
        <Text>{options.unitTicker}</Text>
      </Flex>
      <Box>
        <Text fontWeight='semibold' mr={1}>{t('Description')}:</Text>
        <Box>{options.unitDescription}</Box>
      </Box>
    </Box>
  )
}
