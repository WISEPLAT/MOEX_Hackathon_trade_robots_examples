async ({ deep, require }) => {
  const React = require('react');
  const { Box, Text, Avatar, Wrap, WrapItem } = require('@chakra-ui/react');
  return ({ fillSize, style, link }) => {
    return <div>
      <Box maxW='sm' borderWidth='1px' borderRadius='lg' overflow='hidden' p='4' backgroundColor='white'>
        <Text textAlign="center">Emission</Text>
      </Box>
    </div>;
  }
}