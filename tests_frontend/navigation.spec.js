// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('Navigation - Desktop Routes', () => {
  test('blog link in navigation is present and clickable', async ({ page }) => {
    await page.goto('/');
    
    // Check that Blog link exists in navigation
    const blogLink = page.locator('nav a[href="/posts/"]').first();
    await expect(blogLink).toBeVisible();
    await expect(blogLink).toHaveText(/Blog/);
  });

  test('blog page loads correctly', async ({ page }) => {
    await page.goto('/posts/');
    
    // Check page loads with expected content
    await expect(page).toHaveTitle(/Blog|Journey|A-to-Z/i);
    
    // Check for blog list structure
    const body = await page.locator('body').textContent();
    expect(body).toBeTruthy();
  });

  test('clicking blog link navigates to blog page', async ({ page }) => {
    await page.goto('/');
    
    // Click Blog link in desktop or mobile navigation
    await page.click('nav a[href="/posts/"]');
    
    // Should navigate to /posts/
    await page.waitForURL(/\/posts\//);
    expect(page.url()).toMatch(/\/posts\//);
  });

  test('newsletter preview link in navigation is present and clickable', async ({ page }) => {
    await page.goto('/');
    
    // Check that Newsletter link exists in navigation
    const newsletterLink = page.locator('nav a[href="/newsletter-preview/"]').first();
    await expect(newsletterLink).toBeVisible();
    await expect(newsletterLink).toHaveText(/Newsletter/);
  });

  test('newsletter preview page loads correctly', async ({ page }) => {
    await page.goto('/newsletter-preview/');
    
    // Check page loads
    await expect(page).toHaveTitle(/Newsletter|Preview/i);
    
    // Check for content
    const body = await page.locator('body').textContent();
    expect(body).toBeTruthy();
  });

  test('clicking newsletter link navigates to newsletter preview page', async ({ page }) => {
    await page.goto('/');
    
    // Click Newsletter link in navigation
    await page.click('nav a[href="/newsletter-preview/"]');
    
    // Should navigate to /newsletter-preview/
    await page.waitForURL(/\/newsletter-preview\//);
    expect(page.url()).toMatch(/\/newsletter-preview\//);
  });

  test('my watchlist link in navigation is present and clickable', async ({ page }) => {
    await page.goto('/');
    
    // Check that My Watchlist link exists in navigation
    const watchlistLink = page.locator('nav a[href="/watchlist-preview/"]').first();
    await expect(watchlistLink).toBeVisible();
    await expect(watchlistLink).toHaveText(/Watchlist/);
  });

  test('my watchlist preview page loads correctly', async ({ page }) => {
    await page.goto('/watchlist-preview/');
    
    // Check page loads
    await expect(page).toHaveTitle(/Watchlist|Preview/i);
    
    // Check for content
    const body = await page.locator('body').textContent();
    expect(body).toBeTruthy();
  });

  test('clicking my watchlist link navigates to watchlist preview page', async ({ page }) => {
    await page.goto('/');
    
    // Click My Watchlist link in navigation
    await page.click('nav a[href="/watchlist-preview/"]');
    
    // Should navigate to /watchlist-preview/
    await page.waitForURL(/\/watchlist-preview\//);
    expect(page.url()).toMatch(/\/watchlist-preview\//);
  });

  test('all navigation links are accessible from any page', async ({ page }) => {
    // Start from blog page
    await page.goto('/posts/');
    
    // Navigation should still be present
    const blogLink = page.locator('nav a[href="/posts/"]').first();
    await expect(blogLink).toBeVisible();
    
    const newsletterLink = page.locator('nav a[href="/newsletter-preview/"]').first();
    await expect(newsletterLink).toBeVisible();
    
    const watchlistLink = page.locator('nav a[href="/watchlist-preview/"]').first();
    await expect(watchlistLink).toBeVisible();
  });
});

test.describe('Navigation - Mobile Footer Navigation', () => {
  test.use({ viewport: { width: 375, height: 667 } });

  test('mobile footer navigation is visible on mobile screens', async ({ page }) => {
    await page.goto('/');

    const mobileFooter = page.locator('footer nav[aria-label="Mobile main menu"]');
    await expect(mobileFooter).toBeVisible();

    // Check links in mobile footer
    await expect(mobileFooter.locator('a[href="/"]')).toBeVisible();
    await expect(mobileFooter.locator('a[href="/posts/"]')).toBeVisible();
    await expect(mobileFooter.locator('a[href="/newsletter-preview/"]')).toBeVisible();
    await expect(mobileFooter.locator('a[href="/watchlist-preview/"]')).toBeVisible();
    await expect(mobileFooter.locator('a[href="https://github.com/mekitmedia/cncf-landscape-a-to-z"]')).toBeVisible();
  });

  test('mobile footer links navigate properly', async ({ page }) => {
    await page.goto('/');

    const mobileFooter = page.locator('footer nav[aria-label="Mobile main menu"]');

    // Click Blog in mobile footer
    await mobileFooter.locator('a[href="/posts/"]').click();
    await page.waitForURL(/\/posts\//);
    expect(page.url()).toMatch(/\/posts\//);

    // Click Newsletter in mobile footer
    await mobileFooter.locator('a[href="/newsletter-preview/"]').click();
    await page.waitForURL(/\/newsletter-preview\//);
    expect(page.url()).toMatch(/\/newsletter-preview\//);

    // Click Watchlist in mobile footer
    await mobileFooter.locator('a[href="/watchlist-preview/"]').click();
    await page.waitForURL(/\/watchlist-preview\//);
    expect(page.url()).toMatch(/\/watchlist-preview\//);

    // Click Home in mobile footer
    await mobileFooter.locator('a[href="/"]').click();
    await page.waitForURL(/localhost:1313\/?$/);
  });
});
