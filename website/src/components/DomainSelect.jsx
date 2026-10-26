import React, {useEffect, useId, useRef, useState} from 'react';
import Icon from './Icon';

// Select-only combobox: focus stays on the trigger; the active option is named
// with aria-activedescendant. The popup wraps long labels within the viewport.
export default function DomainSelect({options, value, onChange}) {
  const id = useId(), root = useRef(null), trigger = useRef(null), typeahead = useRef({text: '', time: 0});
  const [open, setOpen] = useState(false), [active, setActive] = useState(0);
  const [placement, setPlacement] = useState({side: 'bottom', height: 320});
  const choices = [{value: 'all', label: 'All domains'}, ...options.map(domain => ({value: domain, label: domain}))];
  const selected = Math.max(0, choices.findIndex(option => option.value === value));

  function show(index = selected) {
    const box = trigger.current.getBoundingClientRect();
    const below = innerHeight - box.bottom - 16, above = box.top - 16;
    const side = below >= 240 || below >= above ? 'bottom' : 'top';
    setPlacement({side, height: Math.max(80, Math.min(352, side === 'bottom' ? below : above))});
    setActive(index); setOpen(true);
  }
  function choose(index) { onChange(choices[index].value); setOpen(false); trigger.current.focus(); }
  useEffect(() => {
    if (!open) return;
    const outside = event => { if (!root.current?.contains(event.target)) setOpen(false); };
    const resize = () => setOpen(false);
    document.addEventListener('pointerdown', outside);
    window.addEventListener('resize', resize);
    return () => { document.removeEventListener('pointerdown', outside); window.removeEventListener('resize', resize); };
  }, [open]);
  useEffect(() => {
    if (open) document.getElementById(`${id}-option-${active}`)?.scrollIntoView({block: 'nearest'});
  }, [open, active, id]);
  function keyDown(event) {
    const {key} = event;
    if (key === 'Tab') { setOpen(false); return; }
    if (key === 'Escape') { if (open) { event.preventDefault(); event.stopPropagation(); setOpen(false); } return; }
    if (['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(key)) {
      event.preventDefault();
      const index = key === 'Home' ? 0 : key === 'End' ? choices.length - 1 : Math.max(0, Math.min(choices.length - 1, active + (key === 'ArrowDown' ? 1 : -1)));
      if (!open) show(key === 'Home' ? 0 : key === 'End' ? choices.length - 1 : selected);
      else setActive(index);
      return;
    }
    if (key === 'Enter' || key === ' ') { event.preventDefault(); if (open) choose(active); else show(); return; }
    if (key.length === 1 && !event.ctrlKey && !event.metaKey && !event.altKey) {
      event.preventDefault();
      const now = Date.now(), previous = typeahead.current;
      const text = (now - previous.time < 700 ? previous.text : '') + key.toLowerCase();
      typeahead.current = {text, time: now};
      const index = choices.findIndex(option => option.label.toLowerCase().startsWith(text));
      if (index >= 0) { if (open) setActive(index); else show(index); }
    }
  }
  return <div className="domain-field" ref={root} onBlur={event => { if (!event.currentTarget.contains(event.relatedTarget)) setOpen(false); }}>
    <label id={`${id}-label`} htmlFor={`${id}-trigger`}>Domain</label>
    <button ref={trigger} id={`${id}-trigger`} className="domain-trigger" type="button" role="combobox"
      aria-labelledby={`${id}-label`} aria-haspopup="listbox" aria-expanded={open}
      aria-controls={`${id}-list`} aria-activedescendant={open ? `${id}-option-${active}` : undefined}
      onClick={() => open ? setOpen(false) : show()} onKeyDown={keyDown}>
      <span>{choices[selected].label}</span><Icon name="chevronDown"/>
    </button>
    {open && <div id={`${id}-list`} className="domain-options" role="listbox" aria-labelledby={`${id}-label`}
      data-side={placement.side} style={{maxHeight: placement.height}}>
      {choices.map((option, index) => <div key={option.value} id={`${id}-option-${index}`} role="option"
        aria-selected={value === option.value} data-active={active === index}
        onPointerMove={() => setActive(index)} onMouseDown={event => event.preventDefault()} onClick={() => choose(index)}>
        <span>{option.label}</span>{value === option.value && <Icon name="check"/>}
      </div>)}
    </div>}
  </div>;
}
