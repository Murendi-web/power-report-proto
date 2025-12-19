def generate_ai_summary(stock_data):
    low = [s for s in stock_data if s["Stock"] < 10]

    summary = []
    if low:
        summary.append("⚠️ LOW STOCK ALERT:")
        for item in low:
            summary.append(f"- {item['Product']} ({item['Stock']} units left)")
    else:
        summary.append("✅ All products have healthy stock levels.")

    avg = sum(s["Stock"] for s in stock_data) / len(stock_data)
    summary.append(f"\n📊 Average stock level: {avg:.1f}")

    return "\n".join(summary)
