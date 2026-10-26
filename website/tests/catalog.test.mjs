import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {filterRecords,paginate} from '../src/lib/catalog.mjs';

const catalog=JSON.parse(await readFile(new URL('../src/data/catalog.json',import.meta.url),'utf8'));
test('combined catalog retains every specialist and profession',()=>{
 assert.equal(catalog.stats.agency,283);assert.equal(catalog.stats.professions,1923);assert.equal(catalog.stats.total,2206);
 assert.equal(new Set(catalog.records.map(r=>r.id)).size,2206);
});
test('visitors can find a role using a capability query and library filter',()=>{
 const results=filterRecords(catalog.records,{query:'software developer',type:'profession',skillsOnly:true});
 assert.ok(results.some(r=>r.title==='Software Developer'));
 assert.ok(results.every(r=>r.hasSkill&&r.type==='profession'));
});
test('empty searches and pagination do not leak stale results',()=>{
 const results=filterRecords(catalog.records,{query:'zznonexistentcapabilityzz'});
 assert.equal(results.length,0);assert.deepEqual(paginate(results,7).items,[]);
 const last=paginate(catalog.records,999);assert.equal(last.page,last.totalPages);assert.ok(last.items.length>0);
});

test('each displayed domain selects its exact nonempty group',()=>{
 for(const domain of new Set(catalog.records.map(record=>record.domain))){
  assert.equal(domain,domain.trim());
  const expected=catalog.records.filter(record=>record.domain===domain);
  assert.deepEqual(filterRecords(catalog.records,{domain}),expected);
  assert.ok(expected.length>0);
 }
});
test('role documents and companion skills are available as inert JSON',async()=>{
 const role=catalog.records.find(r=>r.title==='Software Developer'&&r.type==='profession');
 const artifact=JSON.parse(await readFile(new URL('../static/catalog/'+role.id+'.json',import.meta.url),'utf8'));
 assert.match(artifact.agent,/Core Mission/);assert.match(artifact.skill,/name: software-developer-m1805/);
 assert.match(artifact.expertise,/Activities and Skills/);assert.match(artifact.practice,/Validation Scenarios/);
 assert.doesNotMatch(artifact.agent,/France Travail|\bROME\b|\bBUT\b|SAÉ/);
});
