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

test('domain options wrap inside the viewport and filter the cards',async({page})=>{
 await page.setViewportSize({width:320,height:800});
 await page.goto('./explorer/');
 const domain=page.getByRole('combobox',{name:'Domain',exact:true});
 await domain.click();
 const list=page.getByRole('listbox',{name:'Domain',exact:true});
 await expect(list).toBeVisible();
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
