async ({ deep, require }) => {
  const React = require('react');
  const { Box, Text, Avatar, Wrap, WrapItem } = require('@chakra-ui/react');
  return ({ fillSize, style, link }) => {
    return <div>
      <Box maxW='sm' borderWidth='1px' borderRadius='lg' overflow='hidden' p='4' backgroundColor='white'>
        <Text textAlign="center">Аккаунт на Binance</Text>
        <Wrap>
          <WrapItem>
            <Avatar size='2xl' name='Binance' src='https://altcoinsbox.com/wp-content/uploads/2023/01/black-binance-usd-busd-logo.webp' mb='1' />{' '}
          </WrapItem>
        </Wrap>
      </Box>
    </div>;
  }
}