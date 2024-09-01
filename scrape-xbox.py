from playwright.sync_api import sync_playwright
import csv

def load_xbox_games_page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.xbox.com/en-us/games/all-games?cat=all")

        page.wait_for_load_state("networkidle")  

        # Locate the 'ul' element by its ID
        platform_select_ul = page.locator("#platSelect")

        # Find the 'a' element within the 'ul' that has a 'span' with the text "Xbox Series X|S"
        xbox_series_link = platform_select_ul.locator("a", has=page.locator("span", has_text="Xbox Series X|S"))

        # Click the link
        xbox_series_link.click()

        # Locate the 'div' element with class "paginateControl"
        paginate_control = page.locator("div.paginateControl")

        # Find the button within the paginate control
        paginate_button = paginate_control.locator("button")

        # Click the button to open the dropdown
        paginate_button.click()

        filter_menu_div = paginate_control.locator("ul.c-menu")

        # Find the 'li' item with class "c-menu-item" that has a 'span' containing a 'p' with the text "200 games per page"
        games_per_page_option = filter_menu_div.locator("li.c-menu-item", has=page.locator("span p", has_text="200 games per page"))

        # Click the list item to select the option
        games_per_page_option.click()

        game_titles = []  # Create an empty list to store games

        while True:  # Loop until there's no "Next" pagination link
            
            # Wait for the 'div' elements with class "gameDiv" to appear
            page.wait_for_selector("div.gameDiv")

            # Get all the 'div' elements with class "gameDiv"
            game_divs = page.locator("div.gameDiv")

            # Iterate over each 'div.gameDiv' and print the inner text of the 'h3' inside it
            for i in range(game_divs.count()):
                try:
                    game_div = game_divs.nth(i)
                    h3_element = game_div.locator("h3")
                    game_title = h3_element.inner_text()
                    img_element = game_div.locator("picture img.c-image")
                    cover_url = "https:" + img_element.get_attribute("src").split("?")[0]
                    game_data = {'title': game_title, 'cover_url': cover_url}
                    game_titles.append(game_data)
                except Exception as e:
                        print(f"Error extracting data for game {i}: {e}")

            # Check if the "Next" pagination link exists
            next_page_link = page.locator("li.paginatenext:not(.pag-disabled)")
            if next_page_link.count() == 0:
                break  # Exit the loop if there's no "Next" link

            # Click the "Next" link
            next_page_link.click()

        with open('xbox_game_titles.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Game Title','Cover URL'])  # Write the header row
            for game in game_titles:
                writer.writerow([game['title'], game['cover_url'] ])

        browser.close()

if __name__ == "__main__":
    load_xbox_games_page()