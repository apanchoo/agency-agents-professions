import React from 'react';
import Components from '@theme-original/MDXComponents';
import Heading from '@theme/MDXComponents/Heading';
import Icon from '../components/Icon';

export default {
  ...Components,
  h1: ({children, ...props}) => <Heading as="h1" {...props}><Icon name="book" className="doc-title-icon"/>{children}</Heading>,
};
