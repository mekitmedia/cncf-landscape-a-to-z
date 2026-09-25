import { test, expect } from '@playwright/test';

test.describe('Stats Page - Ecosystem Analytics & Workflow Progress', () => {
  test('stats page loads and displays key metrics and progress table', async ({ page }) => {
    await page.goto('/stats/');

    // Check page title / header banner
    await expect(page.getByRole('heading', { name: 'CNCF Ecosystem & Workflow Insights' })).toBeVisible();

    // Check high-level metric cards
    await expect(page.getByText('Total CNCF Tools')).toBeVisible();
    await expect(page.getByText('Active Categories')).toBeVisible();
    await expect(page.getByText('Tasks Completed')).toBeVisible();
    await expect(page.getByText('Blog Posts Done')).toBeVisible();

    // Check project maturity section
    await expect(page.getByText('CNCF Project Maturity')).toBeVisible();
    await expect(page.getByText('Graduated')).toBeVisible();
    await expect(page.getByText('Incubating')).toBeVisible();
    await expect(page.getByText('Sandbox')).toBeVisible();

    // Check A-Z workflow progress table
    await expect(page.getByText('A-to-Z Research & Workflow Progress')).toBeVisible();
    await expect(page.getByRole('link', { name: 'Letter A' }).first()).toBeVisible();
  });
});
