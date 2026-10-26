import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import {Box, Flex, Text, Button} from '@chakra-ui/react';
import catalog from '../data/catalog.json';

const examples=[['Software Developer','profession','Turn requirements into working, verifiable software.'],['Frontend Developer','agency','Shape accessible interfaces with a focused specialist.'],['Industrial Quality Manager','profession','Connect process controls to measurable acceptance criteria.']];
export default function Home(){
 return <Layout title="Expertise, ready to work" description="Explore 2,206 specialist and professional agents with 1,923 practical skills.">
  <main className="agency-home">
   <section className="hero-grid">
    <Box className="hero-copy">
     <Text className="eyebrow"><span className="status-dot"/> THE PROFESSIONAL AGENT LIBRARY</Text>
     <h1>EXPERTISE,<br/><span>READY TO WORK.</span></h1>
     <Text className="hero-description">A complete professional bench. Pair the precision of a specialist with the depth of a profession — then put both to work.</Text>
     <Flex gap="3" flexWrap="wrap" className="hero-actions">
      <Button asChild className="primary-action"><Link to="/explorer">Explore the library <span aria-hidden="true">↗</span></Link></Button>
      <Button asChild className="secondary-action"><Link to="/docs/intro">Read the field guide →</Link></Button>
     </Flex>
     <div className="hero-footnote">OPEN SOURCE <span>·</span> ENGLISH LANGUAGE <span>·</span> BUILT FOR REAL ASSIGNMENTS</div>
    </Box>
    <Box className="hero-specimen">
     <div className="specimen-top"><span>FIELD NOTES / 001</span><span>↗</span></div>
     <div className="specimen-symbol" aria-hidden="true">a<span>↗</span></div>
     <div className="specimen-label">THE RIGHT ROLE.<br/>THE RIGHT METHOD.<br/>A USEFUL RESULT.</div>
     <div className="specimen-code"><span>ROLE</span> Software Developer<br/><span>MODE</span> Build → verify → deliver<br/><span>STATUS</span> <b>Ready for assignment</b></div>
    </Box>
   </section>
   <section className="metrics" aria-label="Library statistics">
    {[[catalog.stats.total,'AGENTS, ONE LIBRARY'],[catalog.stats.agency,'FOCUSED SPECIALISTS'],[catalog.stats.professions,'PROFESSIONAL ROLES'],[catalog.stats.skills,'COMPANION SKILLS']].map(([value,label])=><div key={label}><strong>{value.toLocaleString('en-US')}</strong><span>{label}</span></div>)}
   </section>
   <section className="editorial-section"><div><Text className="eyebrow">01 / TWO LENSES, ONE ASSIGNMENT</Text><h2>Go narrow.<br/>Think complete.</h2></div><div className="editorial-copy"><p>Some tasks need deep knowledge of a framework, a platform or a discipline. Others need the full perspective of a professional role.</p><p>Agency specialists bring technical precision. Profession agents add the workflows, working knowledge and acceptance criteria that connect the task to its outcome.</p><Link to="/docs/agents-and-skills">Understand agents and skills <span aria-hidden="true">↗</span></Link></div></section>
   <section className="role-section"><div className="section-heading"><Text className="eyebrow">02 / FIND YOUR STARTING POINT</Text><Link to="/explorer">View every role ↗</Link></div><div className="example-grid">{examples.map(([title,type,description],i)=><Link className="example-card" key={title} to={`/explorer?q=${encodeURIComponent(title)}&type=${type}`}><span className="card-number">0{i+1} / {type.toUpperCase()}</span><h3>{title}</h3><p>{description}</p><span className="card-arrow" aria-hidden="true">↗</span></Link>)}</div></section>
   <section className="workflow-strip"><Text className="eyebrow">03 / A SMALL, REPEATABLE WORKFLOW</Text><div>{[['01','Choose a role','Search by profession, capability or domain.'],['02','Load the skill','Bring the practical methods into the assignment.'],['03','Check the outcome','Use evidence and acceptance criteria to assess the result.']].map(([number,title,text])=><article key={number}><span>{number}</span><h3>{title}</h3><p>{text}</p></article>)}</div></section>
   <section className="closing"><h2>Your next assignment<br/>deserves a better starting point.</h2><Link className="closing-link" to="/explorer">Find your agent <span aria-hidden="true">↗</span></Link></section>
  </main>
 </Layout>;
}
