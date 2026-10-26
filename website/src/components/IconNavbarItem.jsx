import React from 'react';
import DefaultNavbarItem from '@theme/NavbarItem/DefaultNavbarItem';
import Icon from './Icon';

export default function IconNavbarItem({icon, label, ...props}) {
  return <DefaultNavbarItem {...props} label={<span className="icon-label"><Icon name={icon}/><span>{label}</span></span>}/>;
}
