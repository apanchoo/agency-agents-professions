import React from 'react';
import Icon from './Icon';

const domains = {
  Academic: 'cap', Design: 'palette', Engineering: 'code', Finance: 'chart', GIS: 'globe',
  'Game Development': 'game', Healthcare: 'heart', Marketing: 'megaphone', 'Paid Media': 'megaphone',
  Product: 'box', 'Project Management': 'briefcase', Research: 'flask', Sales: 'chart', Security: 'shield',
  'Spatial Computing': 'globe', Specialized: 'briefcase', Support: 'people', Testing: 'flask',
  'Agriculture, nature and animals': 'leaf', 'Banking, insurance and real estate': 'building',
  'Business support functions': 'briefcase', 'Commerce and sales': 'chart', 'Communication and media': 'megaphone',
  'Construction and public works': 'building', 'Crafts and arts and crafts': 'palette', Health: 'heart',
  'Hospitality, catering, tourism and entertainment': 'ticket', Industry: 'factory',
  'Installation and maintenance': 'wrench', 'Personal and community services': 'people', Show: 'ticket',
  'Transport and logistics': 'truck',
};

export default function DomainIcon({domain}) {
  return <span className="domain-icon" aria-hidden="true"><Icon name={domains[domain?.trim()] ?? 'briefcase'}/></span>;
}
