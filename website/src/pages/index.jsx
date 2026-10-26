import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import {Box, Flex, Text, Button} from '@chakra-ui/react';
import catalog from '../data/catalog.json';
import Icon from '../components/Icon';

const examples=[['Software Developer','profession','Turn requirements into working, verifiable software.','code'],['Frontend Developer','agency','Shape accessible interfaces with a focused specialist.','palette'],['Industrial Quality Manager','profession','Connect process controls to measurable acceptance criteria.','factory']];
export default function Home(){
 return <Layout title="Expertise, ready to work" description="Explore 2,206 specialist and professional agents with 1,923 practical skills.">
  <main className="agency-home">
   <section className="hero-grid">
    <Box className="hero-copy">
     <Text className="eyebrow"><span className="status-dot"/> THE PROFESSIONAL AGENT LIBRARY</Text>
     <h1>EXPERTISE,<br/><span>READY TO WORK.</span></h1>
     <Text className="hero-description">A complete professional bench. Pair the precision of a specialist with the depth of a profession — then put both to work.</Text>
     <Flex gap="3" flexWrap="wrap" className="hero-actions">
      <Button asChild className="primary-action"><Link to="/explorer">Explore the library <Icon name="arrowUpRight"/></Link></Button>
      <Button asChild className="secondary-action"><Link to="/docs/intro"><Icon name="book"/> Read the field guide</Link></Button>
     </Flex>
     <div className="hero-footnote">OPEN SOURCE <span>·</span> ENGLISH LANGUAGE <span>·</span> BUILT FOR REAL ASSIGNMENTS</div>
    </Box>
    <Box className="hero-specimen">
     <div className="specimen-top"><span>FIELD NOTES / 001</span><span><Icon name="arrowUpRight"/></span></div>
     <div className="specimen-symbol" aria-hidden="true">a<span><Icon name="arrowUpRight"/></span></div>
     <div className="specimen-label">THE RIGHT ROLE.<br/>THE RIGHT METHOD.<br/>A USEFUL RESULT.</div>
     <div className="specimen-code"><span>ROLE</span> Software Developer<br/><span>MODE</span> Build, verify, deliver<br/><span>STATUS</span> <b>Ready for assignment</b></div>
    </Box>
   </section>
   <section className="metrics" aria-label="Library statistics">
    {[[catalog.stats.total,'AGENTS, ONE LIBRARY','layers'],[catalog.stats.agency,'FOCUSED SPECIALISTS','people'],[catalog.stats.professions,'PROFESSIONAL ROLES','briefcase'],[catalog.stats.skills,'COMPANION SKILLS','toolbox']].map(([value,label,icon])=><div key={label}><div className="metric-value"><Icon name={icon}/><strong>{value.toLocaleString('en-US')}</strong></div><span>{label}</span></div>)}
   </section>
   <section className="editorial-section"><div><Text className="eyebrow">01 / TWO LENSES, ONE ASSIGNMENT</Text><h2>Go narrow.<br/>Think complete.</h2></div><div className="editorial-copy"><p>Some tasks need deep knowledge of a framework, a platform or a discipline. Others need the full perspective of a professional role.</p><p>Agency specialists bring technical precision. Profession agents add the workflows, working knowledge and acceptance criteria that connect the task to its outcome.</p><Link to="/docs/agents-and-skills">Understand agents and skills <Icon name="arrowUpRight"/></Link></div></section>
   <section className="role-section"><div className="section-heading"><Text className="eyebrow">02 / FIND YOUR STARTING POINT</Text><Link to="/explorer">View every role <Icon name="arrowUpRight"/></Link></div><div className="example-grid">{examples.map(([title,type,description,icon],i)=><Link className="example-card" key={title} to={`/explorer?q=${encodeURIComponent(title)}&type=${type}`}><div className="example-meta"><span className="example-icon"><Icon name={icon}/></span><span className="card-number">0{i+1} / {type.toUpperCase()}</span></div><h3>{title}</h3><p>{description}</p><span className="card-arrow" aria-hidden="true"><Icon name="arrowUpRight"/></span></Link>)}</div></section>
   <section className="workflow-strip"><Text className="eyebrow">03 / A SMALL, REPEATABLE WORKFLOW</Text><div>{[['01','Choose a role','Search by profession, capability or domain.','compass'],['02','Load the skill','Bring the practical methods into the assignment.','toolbox'],['03','Check the outcome','Use evidence and acceptance criteria to assess the result.','check']].map(([number,title,text,icon])=><article key={number}><div className="workflow-meta"><Icon name={icon}/><span>{number}</span></div><h3>{title}</h3><p>{text}</p></article>)}</div></section>
   <section className="closing"><h2>Your next assignment<br/>deserves a better starting point.</h2><Link className="closing-link" to="/explorer">Find your agent <Icon name="arrowUpRight"/></Link></section>
  </main>
 </Layout>;
}
