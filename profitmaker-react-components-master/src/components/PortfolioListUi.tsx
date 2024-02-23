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
import { useTranslation } from 'react-i18next'

export const PortfolioListUi = ({
  search,
  setSearch,
  data,
  setData,
}: {
  search: string;
  setSearch: (search: string) => void;
  data: any[];
  setData: (data: any[]) => void;
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
            {data.map((item) => (
              <Tr key={item.id}>
                <Td>#{item.id}</Td>
                <Td>
                  <Flex alignItems="center">
                    <Box mr={2}>
                      {item.avatar ? (
                        <Avatar
                          sx={{ width: "24px", height: "24px" }}
                          ml={1}
                          name=""
                          src={item.avatar}
                          mb="1"
                        />
                      ) : (
                        <Box ml={1}>
                          <Identicon linkId={item.id} size={24} />
                        </Box>
                      )}
                    </Box>
                    <Box>{item.name}</Box>
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
