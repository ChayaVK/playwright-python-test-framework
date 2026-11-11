from pathlib import Path

import pytest
from playwright.sync_api import BrowserContext, Dialog, Page, expect

from pages.practice_page import PracticePage

pytestmark = pytest.mark.regression


@pytest.fixture(autouse=True)
def open_practice(practice_page: PracticePage):
    practice_page.open()


def test_accepts_a_js_alert(practice_page: PracticePage, page: Page):
    messages = []

    def handle(dialog: Dialog):
        messages.append(dialog.message)
        dialog.accept()

    page.once("dialog", handle)
    practice_page.alert_button.click()
    assert messages == ["Hello from the Practice Shop"]
    expect(practice_page.result).to_have_text("You saw an alert")


def test_dismisses_a_confirm_box(practice_page: PracticePage, page: Page):
    page.once("dialog", lambda dialog: dialog.dismiss())
    practice_page.confirm_button.click()
    expect(practice_page.result).to_have_text("You clicked: Cancel")


def test_types_into_a_prompt(practice_page: PracticePage, page: Page):
    page.once("dialog", lambda dialog: dialog.accept("Tester"))
    practice_page.prompt_button.click()
    expect(practice_page.result).to_have_text("You entered: Tester")


def test_works_inside_an_iframe(practice_page: PracticePage):
    practice_page.frame.get_by_label("Inside the frame").fill("hello")
    expect(practice_page.frame.locator("#frame-text")).to_have_text("Typed: hello")


def test_handles_a_new_tab(practice_page: PracticePage, context: BrowserContext):
    with context.expect_page() as new_page_info:
        practice_page.new_window_link.click()
    new_page = new_page_info.value
    expect(new_page.locator("#window-heading")).to_have_text("New Window")
    new_page.close()


def test_waits_for_dynamic_content_without_sleeps(practice_page: PracticePage):
    practice_page.start_loading.click()
    expect(practice_page.loaded_text).to_be_visible(timeout=5000)


def test_dropdown_checkbox_and_file_upload(practice_page: PracticePage, upload_file: Path):
    practice_page.country.select_option(label="India")
    expect(practice_page.country).to_have_value("IN")
    practice_page.terms.check()
    expect(practice_page.terms).to_be_checked()
    practice_page.upload.set_input_files(upload_file)
    expect(practice_page.file_name).to_have_text("Uploaded: sample-upload.txt")


def test_reads_the_web_table(practice_page: PracticePage):
    rows = practice_page.table_data()
    assert [r["Name"] for r in rows if r["Department"] == "QA"] == ["Anita", "Carlos"]
    assert max(rows, key=lambda r: int(r["Salary"]))["Name"] == "Elena"
