import {test,expect} from '@playwright/test';
test('find a role, inspect its skill and close with the keyboard',async({page})=>{
 const errors=[];page.on('pageerror',error=>errors.push(error.message));
 await page.goto('./explorer/');
 await page.getByLabel('Search agents and skills').fill('software developer');
 await page.getByLabel('Library',{exact:true}).selectOption('profession');
 await page.getByRole('button').filter({has:page.getByRole('heading',{name:'Software Developer',exact:true})}).click();
 await expect(page.getByRole('dialog')).toBeVisible();
 await page.getByRole('tab',{name:'Skill',exact:true}).click();
 await expect(page.getByRole('dialog').getByRole('heading',{name:'Skills to Apply',exact:true})).toBeVisible();
 await expect(page.getByRole('button',{name:'Copy Markdown'})).toBeEnabled();
 await page.keyboard.press('Escape');await expect(page.getByRole('dialog')).not.toBeVisible();
 expect(errors).toEqual([]);
});
test('search reset and narrow screens remain usable',async({page})=>{
 await page.goto('./explorer/');
 await page.getByLabel('Search agents and skills').fill('zznonexistentcapabilityzz');
 await expect(page.getByRole('heading',{name:'No matching roles.'})).toBeVisible();
 await page.getByRole('button',{name:'Reset filters',exact:true}).first().click();
 await expect(page.getByRole('status').filter({hasText:'roles found'})).toContainText('2,206');
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1);
 expect(overflow).toBe(false);
});
test('landing page leads into the catalog',async({page})=>{
 await page.goto('./');
 await expect(page.getByRole('heading',{name:/EXPERTISE/})).toBeVisible();
 await page.getByRole('link',{name:/Explore the library/}).last().click();
 await expect(page.getByLabel('Search agents and skills')).toBeVisible();
});

test('icon navigation retains its labels and works in the mobile menu',async({page})=>{
 await page.goto('./');
 const toggle=page.getByRole('button',{name:'Toggle navigation bar'});
 if(await toggle.isVisible())await toggle.click();
 await page.getByRole('link',{name:'Documentation',exact:true}).click();
 await expect(page.getByRole('heading',{name:'A professional bench, ready for your next assignment',exact:true})).toBeVisible();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
});

test('domain options wrap inside the viewport and filter the cards',async({page})=>{
 await page.setViewportSize({width:320,height:800});
 await page.goto('./explorer/');
 const domain=page.getByRole('combobox',{name:'Domain',exact:true});
 await domain.click();
 const list=page.getByRole('listbox',{name:'Domain',exact:true});
 await expect(list).toBeVisible();
 await expect(list.getByRole('option')).toHaveCount(33);
 const box=await list.boundingBox();
 expect(box.x).toBeGreaterThanOrEqual(0);expect(box.x+box.width).toBeLessThanOrEqual(321);
 expect(box.y).toBeGreaterThanOrEqual(0);expect(box.y+box.height).toBeLessThanOrEqual(801);
 expect(await list.evaluate(el=>el.scrollWidth<=el.clientWidth+1)).toBe(true);
 await page.getByRole('option',{name:'Hospitality, catering, tourism and entertainment',exact:true}).click();
 await expect(domain).toContainText('Hospitality, catering, tourism and entertainment');
 await expect(list).not.toBeVisible();
 await expect(page.getByRole('status').filter({hasText:'roles found'})).toContainText('119');
 await expect(page.locator('.result-card .domain-icon svg')).toHaveCount(36);
 const domains=await page.locator('.result-card .role-bottom span:first-child').allTextContents();
 expect(new Set(domains)).toEqual(new Set(['Hospitality, catering, tourism and entertainment']));
 await domain.focus();await page.keyboard.press('ArrowDown');
 await expect(list).toBeVisible();await page.keyboard.press('Home');await page.keyboard.press('Enter');
 await expect(domain).toContainText('All domains');await expect(domain).toBeFocused();
 await expect(page.getByRole('status').filter({hasText:'roles found'})).toContainText('2,206');
 await domain.click();await page.keyboard.press('Escape');await expect(list).not.toBeVisible();
 await domain.click();await page.getByRole('heading',{name:'Find the right expertise.'}).click();await expect(list).not.toBeVisible();
});

test('find DevOps by Docker and follow its named technology toolbox',async({page})=>{
 await page.goto('./explorer/');
 await page.getByLabel('Search agents and skills').fill('Docker');
 await page.getByLabel('Library',{exact:true}).selectOption('profession');
 const role=page.getByRole('button').filter({has:page.getByRole('heading',{name:'DevOps Engineer',exact:true})});
 await expect(role).toContainText('Docker');await role.click();
 await page.getByRole('tab',{name:'Technologies',exact:true}).click();
 const panel=page.getByRole('tabpanel',{name:'Technologies',exact:true});
 await expect(panel.getByRole('heading',{name:'Docker Compose',exact:true})).toBeVisible();
 await expect(panel.getByRole('heading',{name:'Terraform',exact:true})).toBeVisible();
 await expect(page.getByRole('link',{name:/View file on GitHub/})).toHaveAttribute('href',/references\/technologies\.md$/);
 await page.getByRole('tab',{name:'Skill',exact:true}).click();
 await page.getByRole('link',{name:'technology toolbox',exact:true}).click();
 await expect(page.getByRole('tab',{name:'Technologies',exact:true})).toHaveAttribute('aria-selected','true');
 await expect(page.getByRole('dialog')).not.toContainText('—');
});

test('AI positioning, source attribution and social sharing metadata are explicit',async({page})=>{
 await page.goto('./');
 await expect(page.getByRole('heading',{name:/AI EXPERTISE/})).toBeVisible();
 await expect(page.getByText('BUILT FROM FRANCE TRAVAIL OPEN DATA',{exact:true})).toBeVisible();
 await expect(page.locator('main')).not.toContainText('—');
 const image=page.locator('meta[property="og:image"]');
 await expect(image).toHaveAttribute('content','https://apanchoo.github.io/agency-agents-professions/img/social-site.png');
 await expect(page.locator('meta[name="twitter:card"]')).toHaveAttribute('content','summary_large_image');
 const asset=await page.request.get('http://127.0.0.1:4173'+new URL(await image.getAttribute('content')).pathname);
 expect(asset.ok()).toBe(true);const bytes=await asset.body();
 expect(bytes.readUInt32BE(16)).toBe(1200);expect(bytes.readUInt32BE(20)).toBe(630);expect(bytes.length).toBeLessThan(1000000);
});
