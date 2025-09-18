# run_example.py (placed at project root)
from finance_agent.agent import FinancialAgent

def main():
    agent = FinancialAgent(verbose=True)
    q = "Tính P/E và ROE của AAPL."
    res = agent.answer(q)
    print("===== FINAL REPORT =====")
    print(res["report"])
    print("\n===== ANSWERED SUBQUESTIONS =====")
    for a in res["answered_subquestions"]:
        print(a)

if __name__ == "__main__":
    main()
