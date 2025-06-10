# Automated Test with Selenium: Google Search

This project demonstrates how to use **Selenium** to automate a browser and perform a Google search.
The program searches for given queries and checks if results appear.
All actions are recorded in a **log file** for later analysis.

---

## 🧰 What is used

- **Python 3.x**
- **Selenium WebDriver**
- **Google Chrome / ChromeDriver**
- **Logging (`logging`)**
- **Waiting for elements (`WebDriverWait`, `expected_conditions`)**
- **Key automation (`Keys`)**
- **Pauses (`time`)**
- **Suppressing the "webdriver" flag** — so that the site does not detect automation

---

## 📋 Functionality

- Go to [https://www.google.com](https://www.google.com)
- Enter text in the search bar
- Press Enter
- Wait for the search result (header `h3`)
- Write the result or error to the console and the file `test_report.log`
