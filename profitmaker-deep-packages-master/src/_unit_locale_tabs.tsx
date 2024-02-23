async ({ deep, require }) => {
  const React = require('react');
  const { useState, useEffect } = React;
  const { HStack, VStack, Box, Text, Avatar, Wrap, WrapItem, Editable, EditablePreview, EditableInput, EditableTextarea, Center, Flex, Divider, Button, Tabs, TabList, TabPanels, Tab, TabPanel, Select, Input } = require('@chakra-ui/react');

  return ({ fillSize, style, link }) => {

    const [langs, setLangs] = useState(['en', 'ru']);


    return <div>
      <Box maxW='sm' minW='sm' w='sm' borderWidth='1px' borderRadius='lg' overflow='hidden' p={4} backgroundColor='white'>
        <Box>
          <Flex
            align="center"
            justify="center"
          >
            <Avatar size='2xl' name='' src={""} mb='1' />
            <Button colorScheme='teal' size='md' variant='outline' sx={{position: 'absolute', right: 4, top: 4,  }}>
              Save
            </Button>
          </Flex>
        </Box>
        <Text>Name: Dogecoin</Text>
        <Text>Ticker: DOGE</Text>
        <text>Description: ...</Text>


        <br />
        <Tabs variant='soft-rounded' colorScheme='green' sx={{
          '&>input:not(:last-child)': {
            marginBottom: 4
          }
        }}>
          <HStack justifyContent='space-between' alignItems='center' mb={4}>
            <TabList>
              <Tab>En</Tab>
              <Tab>Ru</Tab>
            </TabList>
            <Select placeholder='Add lang' w='8rem'>
              <option value='option1'>Uz</option>
              <option value='option2'>Es</option>
              <option value='option3'>Uk</option>
            </Select>
          </HStack>
          <Input w={'100%'} placeholder="Insert Name" />
          <Input w={'100%'} placeholder="Insert Description"/>
        </Tabs>


      </Box>
    </div>;
  }
}