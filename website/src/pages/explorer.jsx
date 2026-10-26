import React,{useEffect,useMemo,useRef,useState} from 'react';
import Layout from '@theme/Layout';
import useBaseUrl from '@docusaurus/useBaseUrl';
import Markdown from 'react-markdown';
import catalog from '../data/catalog.json';
import {filterRecords,paginate} from '../lib/catalog.mjs';

export default function Explorer(){
 const [query,setQuery]=useState(''),[type,setType]=useState('all'),[domain,setDomain]=useState('all'),[skillsOnly,setSkillsOnly]=useState(false),[page,setPage]=useState(1);
 const [selected,setSelected]=useState(null),[content,setContent]=useState(null),[tab,setTab]=useState('agent'),[error,setError]=useState(''),[copied,setCopied]=useState(false);
 const dialog=useRef(null),search=useRef(null);
 const documents=[['agent','Agent'],['skill','Skill'],['expertise','Expertise'],['practice','Methods']].filter(([key])=>key==='agent'||selected?.hasSkill);
 function tabKeyDown(event){
  const keys=['ArrowLeft','ArrowRight','Home','End'];if(!keys.includes(event.key))return;event.preventDefault();
  const index=documents.findIndex(([key])=>key===tab);
  const next=event.key==='Home'?0:event.key==='End'?documents.length-1:(index+(event.key==='ArrowRight'?1:-1)+documents.length)%documents.length;
  setTab(documents[next][0]);setCopied(false);document.getElementById('document-tab-'+documents[next][0])?.focus();
 }
 const base=useBaseUrl('/catalog/');
 const domains=useMemo(()=>[...new Set(catalog.records.map(r=>r.domain))].sort(),[]);
 useEffect(()=>{const params=new URLSearchParams(window.location.search);setQuery(params.get('q')??'');if(['agency','profession'].includes(params.get('type')))setType(params.get('type'));},[]);
 useEffect(()=>setPage(1),[query,type,domain,skillsOnly]);
 const matches=useMemo(()=>filterRecords(catalog.records,{query,type,domain,skillsOnly}),[query,type,domain,skillsOnly]);
 const result=paginate(matches,page);
 useEffect(()=>{if(!selected)return;const controller=new AbortController();setContent(null);setError('');setTab('agent');setCopied(false);dialog.current?.showModal();fetch(base+selected.id+'.json',{signal:controller.signal}).then(r=>{if(!r.ok)throw Error('The role could not be loaded.');return r.json();}).then(setContent).catch(e=>{if(e.name!=='AbortError')setError(e.message);});return()=>controller.abort();},[selected,base]);
 function close(){dialog.current?.close();setSelected(null);setContent(null);}
 function reset(){setQuery('');setType('all');setDomain('all');setSkillsOnly(false);setPage(1);search.current?.focus();}
 async function copy(){try{await navigator.clipboard.writeText(content?.[tab]??'');setCopied(true);}catch{setError('Clipboard access is unavailable. Select and copy the text below.');}}
 return <Layout title="Explore the library" description="Find specialist agents, profession agents and companion skills."><main className="explorer-page">
  <header className="explorer-heading"><div><p className="eyebrow">THE DIRECTORY / {catalog.stats.total.toLocaleString('en-US')} AGENTS</p><h1>Find the right expertise.</h1><p>Search a capability. Choose a role. Get to work.</p></div><a href="https://github.com/apanchoo/agency-agents-professions">Browse the source ↗</a></header>
  <div className="search-bar"><label className="sr-only" htmlFor="agent-search">Search agents and skills</label><span aria-hidden="true">⌕</span><input ref={search} id="agent-search" type="search" placeholder="Try software developer, security, data…" value={query} onChange={e=>setQuery(e.target.value)}/><span className="search-hint">{matches.length.toLocaleString('en-US')} MATCHES</span></div>
  <div className="filter-bar"><label>Library<select aria-label="Library" value={type} onChange={e=>setType(e.target.value)}><option value="all">All agents</option><option value="agency">Agency specialists</option><option value="profession">Professional roles</option></select></label><label>Domain<select aria-label="Domain" value={domain} onChange={e=>setDomain(e.target.value)}><option value="all">All domains</option>{domains.map(d=><option key={d}>{d}</option>)}</select></label><label className="checkbox-label"><input type="checkbox" checked={skillsOnly} onChange={e=>setSkillsOnly(e.target.checked)}/> With companion skill</label><button className="reset-button" onClick={reset}>Reset filters ↺</button></div>
  <div className="results-label" role="status" aria-live="polite"><span>{matches.length.toLocaleString('en-US')} roles found</span><span>ALPHABETICAL / A—Z</span></div>
  {!matches.length?<section className="empty-state"><h2>No matching roles.</h2><p>Try a broader capability or reset your filters.</p><button onClick={reset}>Reset filters</button></section>:<div className="results-grid">{result.items.map(record=><button className="result-card" key={record.id} onClick={()=>setSelected(record)}><div className="role-tags"><span>{record.type==='profession'?'PROFESSION':'SPECIALIST'}</span>{record.hasSkill&&<b>+ SKILL</b>}</div><h2>{record.title}</h2><p>{record.description}</p><div className="role-bottom"><span>{record.domain}</span><span aria-hidden="true">↗</span></div></button>)}</div>}
  <nav className="pagination" aria-label="Catalog pagination"><button disabled={result.page===1} onClick={()=>setPage(p=>p-1)}>← Previous</button><span>Page {result.page} of {result.totalPages}</span><button disabled={result.page===result.totalPages} onClick={()=>setPage(p=>p+1)}>Next →</button></nav>
  <dialog ref={dialog} className="role-dialog" onCancel={close} onClick={e=>{if(e.target===dialog.current)close();}} aria-labelledby="role-title"><div className="dialog-header"><div><p className="eyebrow">{selected?.domain}</p><h2 id="role-title">{selected?.title}</h2></div><button className="close-button" onClick={close} aria-label="Close role details">×</button></div><div className="detail-toolbar"><div className="detail-tabs" role="tablist" aria-label="Role documents">{documents.map(([key,label])=><button key={key} id={'document-tab-'+key} role="tab" aria-controls="document-panel" tabIndex={tab===key?0:-1} onKeyDown={tabKeyDown} aria-selected={tab===key} onClick={()=>{setTab(key);setCopied(false);}}>{label}</button>)}</div><button className="copy-button" disabled={!content} onClick={copy}>{copied?'Copied ✓':'Copy Markdown'}</button></div>{error&&<p role="alert" className="detail-error">{error}</p>}{!content&&!error?<p className="loading-state" role="status">Loading role…</p>:content&&<article id="document-panel" role="tabpanel" aria-labelledby={'document-tab-'+tab} tabIndex={0} className="markdown role-markdown"><Markdown skipHtml>{(content[tab]??'').replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/,'')}</Markdown></article>}<div className="dialog-footer">{content&&<a href={`https://github.com/apanchoo/agency-agents-professions/blob/main/${(tab==='agent'?content.path:tab==='skill'?content.skillPath:content.skillPath.replace(/SKILL\.md$/, 'references/'+(tab==='expertise'?'expertise.md':'practice.md'))).split('/').map(encodeURIComponent).join('/')}`} target="_blank" rel="noopener noreferrer">View file on GitHub ↗</a>}<span>Use the whole skill folder to retain its references.</span></div></dialog>
 </main></Layout>;
}
