import * as React from "react";
import Identicon from "./Identicon";
import {
  Box,
  Input,
  TableContainer,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Flex,
  Avatar,
  useColorModeValue,
} from "@chakra-ui/react";
import { formatNumber } from "../imports/formatNumber";
import { useTranslation } from 'react-i18next'


export const WalletListUi = ({search, setSearch, data}: {
  search: string,
  setSearch: (search: string) => void,
  data: any[]
}) => {
  const bg = useColorModeValue("#fff", "#181818");
  const { t, i18n } = useTranslation()

  return (
    <Box
      maxW="sm"
      minW="sm"
      w="sm"
      borderWidth="1px"
      borderRadius="lg"
      overflow="hidden"
      p={0}
      sx={{ position: "relative" }}
      bg={bg}
    >
      <Box p={4}>
        <Input w={"100%"} placeholder={t('Search')} value={search} onChange={(e) => {setSearch(e.target.value)}}/>
      </Box>
      <TableContainer sx={{maxHeight: '320px', overflowY: 'auto'}}>
        <Table variant="simple">
          <Thead>
            <Tr>
              <Th>{t('Id')}</Th>
              <Th>{t('Name')}</Th>
            </Tr>
          </Thead>
          <Tbody>
            {data.map((wallet) => (
              <Tr key={wallet.id}>
                <Td>#{wallet.id}</Td>
                <Td>
                  <Flex alignItems="center">
                    <Box mr={2}>
                      {wallet.avatar ? (
                        <Avatar
                          sx={{ width: "24px", height: "24px" }}
                          ml={1}
                          name=""
                          src={wallet.avatar}
                          mb="1"
                        />
                      ) : (
                        <Box ml={1}>
                          <Identicon linkId={wallet.id} size={24} />
                        </Box>
                      )}
                    </Box>
                    <Box>
                      <Box>{wallet.name}</Box>
                      <Box>
                        {formatNumber({numberToFormat: wallet.amount, minimumFractionDigits: 2, maximumFractionDigits: 2})} {wallet.unitTicker}
                      </Box>
                    </Box>
                  </Flex>
                </Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </TableContainer>
    </Box>
  );
};
