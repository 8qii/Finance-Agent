# run_example.py (placed at project root)
import sys
import io

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from finance_agent.agent import FinancialAgent

def main():
    agent = FinancialAgent(verbose=False)
    q = "So sánh giá cổ phiếu của APPLE có với Microsoft"
    res = agent.answer(q)
    print("===== FINAL REPORT =====")
    print(res["report"])
    print("\n===== ANSWERED SUBQUESTIONS =====")
    for a in res["answered_subquestions"]:
        print(a)

if __name__ == "__main__":
    main()
