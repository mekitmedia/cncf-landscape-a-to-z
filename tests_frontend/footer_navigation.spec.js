// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('Footer Navigation', () => {
  test('Footer navigation buttons are accessible links', async ({ page }) => {
    await page.goto('/');

    const prevBtn = page.locator('#prev-btn');
    const nextBtn = page.locator('#next-btn');

    await expect(prevBtn).toBeVisible();
    await expect(nextBtn).toBeVisible();

    // Verify they are <a> tags
    const prevTagName = await prevBtn.evaluate(el => el.tagName);
    expect(prevTagName).toBe('A');

    const nextTagName = await nextBtn.evaluate(el => el.tagName);
    expect(nextTagName).toBe('A');

    // Check accessibility attributes
    // If enabled, should have href and aria-disabled="false"
    // If disabled, should not have href and aria-disabled="true"

    const prevDisabled = await prevBtn.getAttribute('aria-disabled');
    if (prevDisabled === 'false') {
        await expect(prevBtn).toHaveAttribute('href');
        await expect(prevBtn).not.toHaveClass(/pointer-events-none/);
    } else {
        await expect(prevBtn).not.toHaveAttribute('href');
        await expect(prevBtn).toHaveClass(/pointer-events-none/);
    }

    const nextDisabled = await nextBtn.getAttribute('aria-disabled');
    if (nextDisabled === 'false') {
        await expect(nextBtn).toHaveAttribute('href');
        await expect(nextBtn).not.toHaveClass(/pointer-events-none/);
    } else {
        await expect(nextBtn).not.toHaveAttribute('href');
        // Locked next button might NOT have pointer-events-none if we want tooltip
        // But end-of-alphabet next button DOES have it.
        // Hard to distinguish without knowing state.
        // But we know it should definitely NOT have href.
    }
  });
});
