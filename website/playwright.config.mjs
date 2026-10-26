import {defineConfig,devices} from '@playwright/test';
export default defineConfig({
 testDir:'tests/browser',timeout:30000,retries:process.env.CI?1:0,
 use:{baseURL:'http://127.0.0.1:4173/agency-agents-professions/',trace:'retain-on-failure'},
 webServer:{command:'npm run serve',url:'http://127.0.0.1:4173/agency-agents-professions/',reuseExistingServer:!process.env.CI,timeout:60000},
 projects:[{name:'desktop',use:{...devices['Desktop Chrome']}},{name:'mobile',use:{...devices['iPhone 13'],defaultBrowserType:'chromium'}}],
});
