import {readFile, readdir, mkdir, writeFile} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const site = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const root = path.dirname(site);
const read = p => readFile(path.join(root, p), 'utf8');
const records = [];
const ids = new Set();
const output = path.join(site, 'static/catalog');
await mkdir(output, {recursive:true});
await mkdir(path.join(site, 'src/data'), {recursive:true});

function field(text, key) {
  const header = /^---\r?\n([\s\S]*?)\r?\n---/.exec(text)?.[1] ?? '';
  let value = new RegExp(`^${key}:\\s*(.+)$`, 'm').exec(header)?.[1]?.trim() ?? '';
  if (value.startsWith('"')) {try{return JSON.parse(value);}catch{}}
  if (value.startsWith("'") && value.endsWith("'")) value=value.slice(1,-1).replaceAll("''", "'");
  return value;
}
async function add(record, content) {
  if(ids.has(record.id)) throw Error(`Duplicate catalog identifier: ${record.id}`);
  record.domain=record.domain.trim();
  record.title=record.title.replaceAll('—','-');
  record.description=record.description.replaceAll('—',',');
  ids.add(record.id);records.push(record);
  await writeFile(path.join(output, record.id+'.json'), JSON.stringify(content));
}
async function walk(directory) {
  const found=[];
  for(const entry of await readdir(path.join(root,directory),{withFileTypes:true})) {
    const relative=directory+'/'+entry.name;
    if(entry.isDirectory())found.push(...await walk(relative));
    else if(entry.name.endsWith('.md'))found.push(relative);
  }
  return found;
}
const divisions=JSON.parse(await read('divisions.json')).divisions;
for(const [division,metadata] of Object.entries(divisions)) {
  if(division==='professions')continue;
  for(const filename of await walk(division)) {
    const agent=await read(filename);
    if(!agent.startsWith('---'))continue;
    const title=field(agent,'name');
    if(!title)throw Error(`Agent title missing: ${filename}`);
    const id='agency-'+filename.slice(0,-3).replaceAll('/','-');
    await add({id,title,description:field(agent,'description'),domain:metadata.label,type:'agency',hasSkill:false,path:filename}, {agent,path:filename});
  }
}
const catalog=JSON.parse(await read('extensions/professions/catalog.json'));
for(const role of catalog) {
  const skillPath='extensions/professions/'+role.skill;
  const refs=path.posix.dirname(skillPath)+'/references/';
  const agentPath=`professions/${role.name}/${role.name}.md`;
  const id='profession-'+role.name;
  await add({id,title:role.title,description:`Professional methods, practical expertise and acceptance criteria for ${role.title}.`,domain:role.domain_title,type:'profession',hasSkill:true,path:agentPath,aliases:role.appellations,technologies:role.technologies??[]}, {
    agent:await read(agentPath),skill:await read(skillPath),expertise:await read(refs+'expertise.md'),practice:await read(refs+'practice.md'),technologies:role.technologies?.length?await read(refs+'technologies.md'):'',path:agentPath,skillPath,
  });
}
records.sort((a,b)=>a.title.localeCompare(b.title,'en'));
const stats={total:records.length,agency:records.filter(r=>r.type==='agency').length,professions:catalog.length,skills:catalog.length,domains:new Set(records.map(r=>r.domain)).size};
const payload={records,stats};
await writeFile(path.join(site,'src/data/catalog.json'),JSON.stringify(payload));
await writeFile(path.join(output,'index.json'),JSON.stringify(payload));
console.log(`Catalog: ${stats.total} agents, ${stats.skills} skills, ${stats.domains} domains`);
