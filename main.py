import requests
from bs4 import BeautifulSoup
import random
import re
import json


def analyze_app_structure(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    forms = soup.find_all("form")
    buttons = soup.find_all("button")
    inputs = soup.find_all("input")

    structure = {
        "forms": [form.get("id", "no_id") for form in forms],
        "buttons": [btn.get_text(strip=True) for btn in buttons],
        "inputs": [inp.get("name") for inp in inputs if inp.get("name")],
    }

    return structure


def generate_test_scenarios(structure):
    test_scenarios = []

    for form in structure["forms"]:
        scenario = {
            "name": f"Проверка формы {form}",
            "steps": [
                {"action": "open_page", "target": form},
                {"action": "fill_form", "data": _generate_input_data(structure["inputs"])},
                {"action": "submit", "target": form},
                {"action": "check_response", "expected": "success"},
            ],
        }
        test_scenarios.append(scenario)

    for button in structure["buttons"]:
        scenario = {
            "name": f"Проверка кнопки '{button}'",
            "steps": [
                {"action": "click", "target": button},
                {"action": "verify_action", "expected": "UI change or redirect"},
            ],
        }
        test_scenarios.append(scenario)

    return test_scenarios


def _generate_input_data(inputs):
    data = {}
    for inp in inputs:
        if re.search("email", inp, re.IGNORECASE):
            data[inp] = f"user{random.randint(1,999)}@example.com"
        elif re.search("pass", inp, re.IGNORECASE):
            data[inp] = "Password123!"
        else:
            data[inp] = "test_value"
    return data


def execute_and_evaluate_tests(test_scenarios):
    results = []
    passed = 0

    for test in test_scenarios:
        success = random.choice([True, True, False])  # имитация 2/3 успешных тестов
        results.append({"test_name": test["name"], "status": "passed" if success else "failed"})
        if success:
            passed += 1

    coverage = round((passed / len(test_scenarios)) * 100, 2)
    report = {
        "total_tests": len(test_scenarios),
        "passed": passed,
        "failed": len(test_scenarios) - passed,
        "coverage_percent": coverage,
        "details": results,
    }

    return report


def main():
    url = "https://httpbin.org/forms/post"

    print("🔍 Анализ структуры приложения...")
    structure = analyze_app_structure(url)

    print("🧠 Генерация тестовых сценариев...")
    scenarios = generate_test_scenarios(structure)

    print("⚙️ Выполнение тестов и оценка эффективности...")
    report = execute_and_evaluate_tests(scenarios)

    print("\n📊 Отчёт о тестировании:")
    print(json.dumps(report, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
