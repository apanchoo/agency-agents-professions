import {test, expect} from '@playwright/test';

// This is a targeted regression suite, not a complete RGAA conformance audit.
async function textIssues(page, selector = 'main, .navbar, .footer') {
  return page.locator(selector).evaluateAll(roots => {
    const rgb = value => (value.match(/[\d.]+/g) || []).map(Number);
    const blend = (front, back) => front.slice(0, 3).map((v, i) => v * (front[3] ?? 1) + back[i] * (1 - (front[3] ?? 1)));
    const luminance = color => color.map(v => v / 255).map(v => v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4).reduce((sum, v, i) => sum + v * [.2126, .7152, .0722][i], 0);
    const issues = [];
    for (const root of roots) for (const el of [root, ...root.querySelectorAll('*')]) {
      if (!Array.from(el.childNodes).some(n => n.nodeType === Node.TEXT_NODE && n.textContent.trim())) continue;
      if (el.closest('[aria-hidden="true"], .sr-only, option, script, style, svg')) continue;
      const box = el.getBoundingClientRect(), style = getComputedStyle(el);
      if (!box.width || !box.height || box.right <= 0 || box.left >= innerWidth || style.visibility !== 'visible') continue;
      const layers = [];
      for (let ancestor = el; ancestor; ancestor = ancestor.parentElement) layers.unshift(rgb(getComputedStyle(ancestor).backgroundColor));
      const background = layers.reduce((back, layer) => blend(layer, back), [255, 255, 255]);
      const foreground = blend(rgb(style.color), background);
      const [light, dark] = [luminance(foreground), luminance(background)].sort((a, b) => b - a);
      const contrast = (light + .05) / (dark + .05);
      const size = parseFloat(style.fontSize);
      if (size < 16 || contrast < 4.5) issues.push({text: el.textContent.trim().slice(0, 65), size, contrast: +contrast.toFixed(2)});
    }
    return issues;
  });
}

for (const [name, route] of [['landing', './'], ['explorer', './explorer/'], ['documentation', './docs/intro/']]) {
  test(`${name}: readable text and contrast`, async ({page}, testInfo) => {
    await page.goto(route);
    await expect(page.locator('main')).toBeVisible();
    expect(await textIssues(page)).toEqual([]);
    await page.screenshot({path: testInfo.outputPath(`${name}.png`)});
  });
}

test('320px reflow, 200% text enlargement and increased text spacing', async ({page}) => {
  for (const route of ['./', './explorer/', './docs/intro/']) {
    await page.setViewportSize({width: 320, height: 800});
    await page.goto(route);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
    await page.setViewportSize({width: 640, height: 800});
    const before = await page.locator('main p').first().evaluate(el => parseFloat(getComputedStyle(el).fontSize));
    await page.addStyleTag({content: 'html{font-size:200%!important}'});
    const after = await page.locator('main p').first().evaluate(el => parseFloat(getComputedStyle(el).fontSize));
    expect(after).toBeGreaterThanOrEqual(before * 1.99);
    await page.addStyleTag({content: '*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}'});
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
    await expect(page.locator('main h1').first()).toBeVisible();
    if (route.includes('explorer')) {
      const domain = page.getByRole('combobox', {name: 'Domain', exact: true});
      await domain.click();
      const list = page.getByRole('listbox', {name: 'Domain', exact: true});
      const bounds = await list.boundingBox();
      expect(bounds.x + bounds.width).toBeLessThanOrEqual(641);
      expect(await list.evaluate(el => el.scrollWidth <= el.clientWidth + 1)).toBe(true);
      expect(await textIssues(page)).toEqual([]);
      await page.keyboard.press('Escape');
      await page.getByLabel('Search agents and skills').fill('software developer');
      await page.getByRole('button').filter({has: page.getByRole('heading', {name: 'Software Developer', exact: true})}).click();
      await expect(page.getByRole('dialog')).toBeVisible();
      expect(await page.getByRole('dialog').evaluate(el => el.scrollWidth <= el.clientWidth + 1)).toBe(true);
      await expect(page.getByRole('button', {name: 'Close role details'})).toBeInViewport();
      await page.keyboard.press('Escape');
    }
  }
});

test('document tabs work with arrow keys, focus is visible and returns to the role', async ({page}) => {
  await page.goto('./explorer/?q=software%20developer&type=profession');
  const role = page.getByRole('button').filter({has: page.getByRole('heading', {name: 'Software Developer', exact: true})});
  await role.focus();
  await page.keyboard.press('Enter');
  await page.getByRole('tab', {name: 'Agent', exact: true}).focus();
  await page.keyboard.press('ArrowRight');
  const skill = page.getByRole('tab', {name: 'Skill', exact: true});
  await expect(skill).toBeFocused();
  await expect(skill).toHaveAttribute('aria-selected', 'true');
  await expect(page.getByRole('tabpanel', {name: 'Skill'})).toBeVisible();
  expect(await skill.evaluate(el => getComputedStyle(el).outlineStyle)).toBe('solid');
  expect(await textIssues(page, '.role-dialog')).toEqual([]);
  await page.keyboard.press('End');
  await expect(page.getByRole('tab', {name: 'Methods', exact: true})).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(role).toBeFocused();
});
