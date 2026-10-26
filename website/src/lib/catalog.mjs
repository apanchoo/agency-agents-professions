export const normalize = value => value.normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
export function filterRecords(records, {query='',type='all',domain='all',skillsOnly=false}={}) {
  const words=normalize(query.trim()).split(/\s+/).filter(Boolean);
  return records.filter(record=>{
    if(type!=='all'&&record.type!==type)return false;
    if(domain!=='all'&&record.domain!==domain)return false;
    if(skillsOnly&&!record.hasSkill)return false;
    const text=normalize([record.title,record.description,record.domain,...(record.aliases??[])].join(' '));
    return words.every(word=>text.includes(word));
  });
}
export function paginate(records,page,size=36) {
  const totalPages=Math.max(1,Math.ceil(records.length/size));
  const currentPage=Math.max(1,Math.min(page,totalPages));
  return {items:records.slice((currentPage-1)*size,currentPage*size),page:currentPage,totalPages};
}
