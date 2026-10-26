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
