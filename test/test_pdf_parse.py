from finance_agent.tools.pdf_parse import parse_financial_report

def test_parse_financial_report_mock():
    result = parse_financial_report("dummy.pdf", ["summary"])
    assert "pdf_path" in result
    assert "content_summary" in result

def test_parse_financial_report_no_path():
    result = parse_financial_report("")
    assert "error" in result
