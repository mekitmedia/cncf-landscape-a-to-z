// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('Letter page - status filters', () => {
  test('filter buttons are visible on letter page', async ({ page }) => {
    await page.goto('/letters/a/');

    const allBtn = page.locator('.filter-btn[data-filter="all"]');
    await expect(allBtn).toBeVisible();

    const graduatedBtn = page.locator('.filter-btn[data-filter="graduated"]');
    await expect(graduatedBtn).toBeVisible();

    const incubatingBtn = page.locator('.filter-btn[data-filter="incubating"]');
    await expect(incubatingBtn).toBeVisible();

    const sandboxBtn = page.locator('.filter-btn[data-filter="sandbox"]');
    await expect(sandboxBtn).toBeVisible();
  });

  test('"All" filter is active by default', async ({ page }) => {
    await page.goto('/letters/a/');

    const allBtn = page.locator('.filter-btn[data-filter="all"]');
    await expect(allBtn).toHaveAttribute('aria-pressed', 'true');
  });

  test('clicking a status filter hides non-matching cards', async ({ page }) => {
    await page.goto('/letters/a/');

    // Click the "graduated" filter
    await page.locator('.filter-btn[data-filter="graduated"]').click();

    // Cards that are NOT graduated should be hidden
    const nonGraduatedCards = page.locator('.project-card:not([data-project="graduated"])');
    const count = await nonGraduatedCards.count();
    for (let i = 0; i < count; i++) {
      await expect(nonGraduatedCards.nth(i)).toBeHidden();
    }
  });

  test('clicking a status filter keeps matching cards visible', async ({ page }) => {
    await page.goto('/letters/a/');

    // Click the "graduated" filter
    await page.locator('.filter-btn[data-filter="graduated"]').click();

    const graduatedCards = page.locator('.project-card[data-project="graduated"]');
    const count = await graduatedCards.count();
    if (count > 0) {
      await expect(graduatedCards.first()).toBeVisible();
    }
  });

  test('clicking "All" restores all cards', async ({ page }) => {
    await page.goto('/letters/a/');

    // First filter to graduated
    await page.locator('.filter-btn[data-filter="graduated"]').click();

    // Then click All
    await page.locator('.filter-btn[data-filter="all"]').click();

    const cards = page.locator('.project-card');
    const count = await cards.count();
    for (let i = 0; i < count; i++) {
      await expect(cards.nth(i)).toBeVisible();
    }
  });

  test('empty category sections are hidden after filtering', async ({ page }) => {
    await page.goto('/letters/a/');

    await page.locator('.filter-btn[data-filter="graduated"]').click();

    // Sections containing only non-graduated projects should be hidden
    const sections = page.locator('.category-section');
    const count = await sections.count();
    for (let i = 0; i < count; i++) {
      const section = sections.nth(i);
      const visibleCards = section.locator('.project-card[data-project="graduated"]');
      const visibleCount = await visibleCards.count();
      if (visibleCount === 0) {
        await expect(section).toBeHidden();
      } else {
        await expect(section).toBeVisible();
      }
    }
  });

  test('active filter button updates aria-pressed attribute', async ({ page }) => {
    await page.goto('/letters/a/');

    await page.locator('.filter-btn[data-filter="incubating"]').click();

    await expect(page.locator('.filter-btn[data-filter="incubating"]')).toHaveAttribute('aria-pressed', 'true');
    await expect(page.locator('.filter-btn[data-filter="all"]')).toHaveAttribute('aria-pressed', 'false');
  });
});
