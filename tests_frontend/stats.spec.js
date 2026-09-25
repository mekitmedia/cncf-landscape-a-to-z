// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('Statistics & Insights Page', () => {
  test('stats page loads and displays header title', async ({ page }) => {
    await page.goto('/stats/');
    await expect(page).toHaveTitle(/CNCF Landscape Ecosystem Insights/i);
    await expect(page.locator('h1')).toContainText('CNCF Landscape Ecosystem Insights');
  });

  test('KPI summary cards are visible', async ({ page }) => {
    await page.goto('/stats/');
    await expect(page.locator('text=TOTAL TOOLS')).toBeVisible();
    await expect(page.locator('text=CNCF HOSTED')).toBeVisible();
    await expect(page.locator('text=DEEP RESEARCHED')).toBeVisible();
    await expect(page.locator('text=PUBLISHED CONTENT')).toBeVisible();
  });

  test('A-Z letter workflow progress grid is rendered', async ({ page }) => {
    await page.goto('/stats/');
    await expect(page.locator('text=A-Z Letter Workflow Progress')).toBeVisible();

    // Check that letter A button/card is present and links to /letters/a/
    const letterACard = page.locator('a[href="/letters/a/"]').first();
    await expect(letterACard).toBeVisible();
  });

  test('navigation bar contains Statistics link', async ({ page }) => {
    await page.goto('/');
    const statsNavLink = page.locator('nav a[href="/stats/"]');
    await expect(statsNavLink).toBeVisible();
    await statsNavLink.click();
    await page.waitForURL(/\/stats\//);
    expect(page.url()).toMatch(/\/stats\//);
  });
});
