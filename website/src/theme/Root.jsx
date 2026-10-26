import React from 'react';
import {ChakraProvider, createSystem, defaultConfig} from '@chakra-ui/react';

const system = createSystem(defaultConfig, {preflight: false});
export default function Root({children}) {
  return <ChakraProvider value={system}>{children}</ChakraProvider>;
}
