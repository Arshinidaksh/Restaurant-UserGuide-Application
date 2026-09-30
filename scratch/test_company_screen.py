from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.goto('https://app.restaurant-pos.isarva.in/', timeout=30000)
    page.wait_for_timeout(2000)
    
    if page.locator('button:has-text("Activate")').count() > 0:
        page.locator('input').first.fill('C001')
        page.locator('button:has-text("Activate")').click()
        page.wait_for_timeout(2000)
        
    if page.locator('button:has-text("OK")').count() > 0:
        inputs = page.locator('input').all()
        inputs[0].fill('admin')
        inputs[1].fill('0000')
        page.locator('button:has-text("OK")').click()
        page.wait_for_timeout(2500)
        
    page.goto('https://app.restaurant-pos.isarva.in/settings', timeout=30000)
    page.wait_for_timeout(2000)
    
    card = page.locator('text=Company Details')
    if card.count() > 0:
        card.first.click()
        page.wait_for_timeout(2000)
        page.screenshot(path='scratch/company_details_screen.jpg', quality=95)
        print('Saved scratch/company_details_screen.jpg')
    else:
        print('Company details not found')
    browser.close()
