// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('Navigation - New Routes', () => {
  test('blog link in navigation is present and clickable', async ({ page }) => {
    await page.goto('/');
    
    // Check that Blog link exists in navigation
    const blogLink = page.locator('nav a[href="/posts/"]');
    await expect(blogLink).toBeVisible();
    await expect(blogLink).toHaveText('Blog');
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
    
    // Click Blog link in navigation
    await page.click('nav a[href="/posts/"]');
    
    // Should navigate to /posts/
    await page.waitForURL(/\/posts\//);
    expect(page.url()).toMatch(/\/posts\//);
  });

  test('newsletter preview link in navigation is present and clickable', async ({ page }) => {
    await page.goto('/');
    
    // Check that Newsletter link exists in navigation
    const newsletterLink = page.locator('nav a[href="/newsletter-preview/"]');
    await expect(newsletterLink).toBeVisible();
    await expect(newsletterLink).toHaveText('Newsletter');
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
    const watchlistLink = page.locator('nav a[href="/watchlist-preview/"]');
    await expect(watchlistLink).toBeVisible();
    await expect(watchlistLink).toHaveText('My Watchlist');
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
    const blogLink = page.locator('nav a[href="/posts/"]');
    await expect(blogLink).toBeVisible();
    
    const newsletterLink = page.locator('nav a[href="/newsletter-preview/"]');
    await expect(newsletterLink).toBeVisible();
    
    const watchlistLink = page.locator('nav a[href="/watchlist-preview/"]');
    await expect(watchlistLink).toBeVisible();
  });
});
