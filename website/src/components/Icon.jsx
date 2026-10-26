import React from 'react';

const paths = {
  briefcase: ['M8 6V4h8v2', 'M3 7h18v14H3z', 'M3 12h18', 'M10 12v3h4v-3'],
  code: ['m8 7-5 5 5 5', 'm16 7 5 5-5 5', 'm14 4-4 16'],
  palette: ['M12 3a9 9 0 1 0 0 18h1a2 2 0 0 0 0-4h-1a2 2 0 0 1 0-4h4a5 5 0 0 0 5-5c0-3-4-5-9-5Z', 'M7 9h.01M10 6h.01M16 7h.01M6 14h.01'],
  shield: ['M12 3 4 6v6c0 5 8 9 8 9s8-4 8-9V6z', 'm8 12 3 3 5-6'],
  heart: ['M20 5c-2-2-6-1-8 2-2-3-6-4-8-2-4 4 1 9 8 15 7-6 12-11 8-15Z', 'M5 12h4l2-3 2 6 2-3h4'],
  chart: ['M4 3v17h17', 'M8 16v-5M13 16V7M18 16V4'],
  people: ['M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2', 'M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8', 'M17 4a4 4 0 0 1 0 8M22 21v-2a4 4 0 0 0-3-4'],
  leaf: ['M20 3C8 2 2 7 4 15c3 8 16 8 16-12Z', 'M4 21 16 9'],
  building: ['M4 21V8l8-5 8 5v13z', 'M9 21v-6h6v6M8 9h.01M16 9h.01'],
  factory: ['M3 21V10l6 4V8l6 4V4h5l1 17z', 'M7 17h1M12 17h1M17 17h1'],
  wrench: ['M21 4a6 6 0 0 1-8 8l-8 8a2 2 0 0 1-3-3l8-8a6 6 0 0 1 8-8l-4 4 4 3z'],
  truck: ['M2 6h12v12H2zM14 10h4l4 4v4h-8', 'M7 20a2 2 0 1 0 0-4 2 2 0 0 0 0 4M18 20a2 2 0 1 0 0-4 2 2 0 0 0 0 4'],
  megaphone: ['M3 10v5h5l12 5V5L8 10z', 'm7 15 2 6h4l-2-5'],
  cap: ['m2 9 10-6 10 6-10 6z', 'M6 12v6c4 3 8 3 12 0v-6M22 9v8'],
  globe: ['M21 12a9 9 0 1 0-18 0 9 9 0 0 0 18 0', 'M3 12h18M12 3c-5 5-5 13 0 18 5-5 5-13 0-18'],
  flask: ['M9 3h6M10 3v6l-6 10a1 1 0 0 0 1 2h14a1 1 0 0 0 1-2L14 9V3', 'M7 15h10'],
  ticket: ['M3 6h18v4a2 2 0 0 0 0 4v4H3v-4a2 2 0 0 0 0-4z', 'M15 6v3M15 12h.01M15 15v3'],
  box: ['m3 7 9-4 9 4v10l-9 4-9-4z', 'm3 7 9 4 9-4M12 11v10M7 5l10 4'],
  game: ['M7 7h10c4 0 7 13 3 13l-5-4H9l-5 4C0 20 3 7 7 7Z', 'M6 10v4M4 12h4M16 11h.01M19 14h.01'],

  search: ['M20 20l-5-5', 'M17 10a7 7 0 1 0-14 0 7 7 0 0 0 14 0'],
  book: ['M12 5v16', 'M12 5C8 2 4 3 2 4v15c4-2 7-1 10 2 3-3 6-4 10-2V4c-2-1-6-2-10 1Z'],
  layers: ['m12 3 10 5-10 5L2 8z', 'm2 12 10 5 10-5M2 16l10 5 10-5'],
  toolbox: ['M3 7h18v14H3z', 'M8 7V3h8v4M3 12h18M9 10v4M15 10v4'],
  compass: ['M21 12a9 9 0 1 0-18 0 9 9 0 0 0 18 0', 'm16 8-3 5-5 3 3-5z'],
  check: ['m5 12 4 4L19 6'],
  copy: ['M8 8h13v13H8z', 'M16 8V3H3v13h5'],
  x: ['m6 6 12 12M6 18 18 6'],
  rotate: ['M20 7v5h-5', 'M20 12a8 8 0 1 0-2 6'],
  arrowUpRight: ['M6 18 18 6M6 6h12v12'],
  arrowRight: ['M4 12h16m-6-6 6 6-6 6'],
  arrowLeft: ['M20 12H4m6-6-6 6 6 6'],
  chevronDown: ['m6 9 6 6 6-6'],
  file: ['M14 2H4v20h16V8z', 'M14 2v6h6M8 13h8M8 17h5'],
  sliders: ['M4 3v7m0 4v7M12 3v12m0 4v2M20 3v3m0 4v11', 'M1 10h6v4H1zM9 15h6v4H9zM17 6h6v4h-6z'],
  download: ['M12 3v12m-5-5 5 5 5-5', 'M3 16v5h18v-5'],
  github: ['M4 3h16v18H4z', 'M8 3v18M12 7h4M12 11h4M12 15h2'],
};

export default function Icon({name, className = ''}) {
  return <svg className={'icon ' + className} data-icon={name} aria-hidden="true" focusable="false"
    viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
    {(paths[name] ?? paths.briefcase).map((path, index) => <path key={index} d={path}/>)}
  </svg>;
}
