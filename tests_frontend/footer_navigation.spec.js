// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('Homepage Footer Navigation', () => {
  test('Previous button is a link (when applicable) and Next button is disabled', async ({ page }) => {
    await page.goto('/');

    // Wait for the letter heading to be visible
    const letterHeadingLocator = page.locator('#current-letter-featured');
    await expect(letterHeadingLocator).toBeVisible();
    const letterHeading = await letterHeadingLocator.textContent();
    const isLetterA = letterHeading?.trim() === 'A';

    const prevBtn = page.locator('#prev-btn');
    const nextBtn = page.locator('#next-btn');

    if (isLetterA) {
      // Previous should be disabled span
      // Note: We use aria-disabled="true" for semantics
      await expect(prevBtn).toHaveAttribute('aria-disabled', 'true');
      // Should not have href
      await expect(prevBtn).not.toHaveAttribute('href');
    } else {
      // Previous should be a link
      await expect(prevBtn).toHaveAttribute('href', /\/letters\/[a-z]\//);
      // Should not be disabled
      await expect(prevBtn).not.toHaveAttribute('aria-disabled', 'true');
    }

    // Next button should ALWAYS be disabled on homepage (as it shows latest week)
    await expect(nextBtn).toHaveAttribute('aria-disabled', 'true');
    // It should be a span, so no href
    await expect(nextBtn).not.toHaveAttribute('href');

    // Check they are visible
    await expect(prevBtn).toBeVisible();
    await expect(nextBtn).toBeVisible();
  });
});
