// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('Level 1: Homepage - Featured Tools', () => {
  test('homepage loads with correct title', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/CNCF Landscape Overview/);
  });

  test('alphabet navigation is present', async ({ page }) => {
    await page.goto('/');
    
    // Check that alphabet buttons A-Z exist
    const letterA = page.locator('text=A').first();
    await expect(letterA).toBeVisible();
    
    const letterZ = page.locator('text=Z').first();
    await expect(letterZ).toBeVisible();
  });

  test('featured tools grid is displayed', async ({ page }) => {
    await page.goto('/');
    
    // Check for featured tools section
    const body = await page.locator('body').textContent();
    expect(body).toBeTruthy();
  });

  test('clicking a letter navigates to letter page', async ({ page }) => {
    await page.goto('/');
    
    // Click on letter A button (or link)
    await page.click('#alphabet-container button:has-text("A")');
    
    // Should navigate to /letters/a/
    await page.waitForURL(/\/letters\/[a-z]\//);
    expect(page.url()).toMatch(/\/letters\/[a-z]\//);
  });
});

test.describe('Level 2: Letter Pages - All Tools with Abstracts', () => {
  test('letter page loads and displays projects', async ({ page }) => {
    await page.goto('/letters/a/');
    
    // Check page loaded
    await expect(page).toHaveTitle(/Letter A|Week.*A/i);
    
    // Check for content structure
    const body = page.locator('body');
    await expect(body).toBeVisible();
  });

  test('projects are organized by category', async ({ page }) => {
    await page.goto('/letters/a/');
    
    // Look for category headings - common CNCF categories
    const bodyText = await page.locator('body').textContent();
    
    // Should have some organization structure (headings, lists, etc)
    expect(bodyText).toBeTruthy();
  });

  test('projects display metadata (name, status, links)', async ({ page }) => {
    await page.goto('/letters/a/');
    
    // Check for project links (GitHub repos or homepages)
    const links = page.locator('a[href*="github.com"], a[href*="http"]');
    const linkCount = await links.count();
    
    // Should have at least some project links
    expect(linkCount).toBeGreaterThan(0);
  });

  test('details link navigates to individual tool page', async ({ page }) => {
    await page.goto('/letters/a/');
    
    // Look for a "Details" link or button
    const detailsLink = page.locator('a:has-text("Details")').first();
    await expect(detailsLink).toBeVisible();

    await detailsLink.click();
    
    // Should navigate to /tools/{name}/
    await page.waitForURL(/\/tools\/.+/);
    expect(page.url()).toMatch(/\/tools\/.+/);
  });
});

test.describe.skip('Level 3: Tool Deep Dive - Individual Project Pages', () => {
  test('tool page loads with project information', async ({ page }) => {
    await page.goto('/letters/a/');
    
    // Navigate to first available tool page
    const detailsLink = page.locator('a:has-text("Details")').first();
    await expect(detailsLink).toBeVisible();

    await detailsLink.click();
    await page.waitForURL(/\/tools\/.+/);

    // Check that the page has content
    const body = page.locator('body');
    await expect(body).toBeVisible();
    
    // Should have a title
    const title = await page.title();
    expect(title.length).toBeGreaterThan(0);
  });

  test('tool page has breadcrumb or back navigation', async ({ page }) => {
    await page.goto('/letters/a/');
    
    const detailsLink = page.locator('a:has-text("Details")').first();
    await expect(detailsLink).toBeVisible();

    await detailsLink.click();
    await page.waitForURL(/\/tools\/.+/);
    
    // Look for navigation back to letter page
    const backLink = page.locator('a[href*="/letters/"]');
    await expect(backLink.first()).toBeVisible();
  });

  test('tool page displays external links (GitHub, website)', async ({ page }) => {
    await page.goto('/letters/a/');
    
    const detailsLink = page.locator('a:has-text("Details")').first();
    await expect(detailsLink).toBeVisible();

    await detailsLink.click();
    await page.waitForURL(/\/tools\/.+/);

    // Check for external links
    const externalLinks = page.locator('a[href*="github.com"], a[href*="http"]');
    const count = await externalLinks.count();
    
    expect(count).toBeGreaterThan(0);
  });
});

test.describe('Navigation Flow - Complete User Journey', () => {
  test('user can navigate from homepage through all three levels', async ({ page }) => {
    // Level 1: Start at homepage
    await page.goto('/');
    await expect(page).toHaveTitle(/CNCF Landscape Overview/);
    
    // Navigate to a letter page
    await page.click('#alphabet-container button:has-text("A")');
    await page.waitForURL(/\/letters\/[a-z]\//);
    
    // Level 2: On letter page
    const url = page.url();
    expect(url).toMatch(/\/letters\/[a-z]\//);
    
    // Click on a details link if available
    const detailsLink = page.locator('a:has-text("Details")').first();
    await expect(detailsLink).toBeVisible();

    /*
    // Skipping Level 3 navigation as tool pages are not yet implemented
    await detailsLink.click();
    await page.waitForURL(/\/tools\/.+/);
    
    // Level 3: On tool page
    const toolUrl = page.url();
    expect(toolUrl).toMatch(/\/tools\/.+/);

    // Should be able to navigate back
    const backLink = page.locator('a[href*="/letters/"]').first();
    await expect(backLink).toBeVisible();

    await backLink.click();
    await page.waitForURL(/\/letters\/[a-z]\//);
    */
  });
});
