// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('Hugo Site Tests', () => {
  test('homepage loads successfully', async ({ page }) => {
    await page.goto('/');

    // Check that the page has loaded and contains the site title
    await expect(page).toHaveTitle(/My New Hugo Site/);
  });

  test('homepage has content', async ({ page }) => {
    await page.goto('/');

    // Check that the page has some visible content
    const body = page.locator('body');
    await expect(body).toBeVisible();
  });

  test('navigation is accessible', async ({ page }) => {
    await page.goto('/');

    // Check that basic HTML structure exists
    await expect(page.locator('html')).toBeVisible();
  });
});
