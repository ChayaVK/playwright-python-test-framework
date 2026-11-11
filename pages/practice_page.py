from playwright.sync_api import Page

from pages.base_page import BasePage


class PracticePage(BasePage):
    """Practice page: alerts, frames, windows, waits, dropdown, checkbox, upload and a web table."""

    path = "practice.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.alert_button = page.get_by_role("button", name="JS Alert")
        self.confirm_button = page.get_by_role("button", name="JS Confirm")
        self.prompt_button = page.get_by_role("button", name="JS Prompt")
        self.result = page.locator("#alert-result")
        self.frame = page.frame_locator("#practice-frame")
        self.new_window_link = page.get_by_role("link", name="Open new window")
        self.start_loading = page.get_by_role("button", name="Start")
        self.loaded_text = page.locator("#loaded-text")
        self.country = page.get_by_label("Country")
        self.terms = page.get_by_label("I accept the terms")
        self.upload = page.locator("#file-upload")
        self.file_name = page.locator("#file-name")
        self.table_rows = page.locator("#employees tbody tr")

    def table_data(self) -> list[dict[str, str]]:
        """Reads the web table into dicts, for example {"Name": "Anita", "Department": "QA", "Salary": "65000"}."""
        headers = self.texts(self.page.locator("#employees thead th"))
        return [dict(zip(headers, self.texts(row.locator("td")))) for row in self.table_rows.all()]
