import json

conf = json.load(open("config.json"))

def inp(key):
    global conf
    return conf[key]


portfolio = int(inp("current_holdings"))
p_inter = int(inp("percentage_international_stock")) * 0.01
p_bond = int(inp("percentage_bond")) * 0.01

monthly_d = int(inp("monthly_domestic_stock_contribution"))
monthly_i = int(inp("monthly_international_stock_contribution"))
monthly_b = int(inp("monthly_bond_contribution"))

bond_yield = int(inp("expected_bond_return_percentage")) * 0.01
d_stock_yield = int(inp("expected_domestic_stock_return_percentage")) * 0.01
f_stock_yield = int(inp("expected_international_stock_return_percentage")) * 0.01

bond_yield = (1 + bond_yield) ** (1 / 12) - 1
d_stock_yield = (1 + d_stock_yield) ** (1 / 12) - 1
f_stock_yield = (1 + f_stock_yield) ** (1 / 12) - 1

current_bond = (portfolio * p_bond)
current_stock = portfolio - current_bond
i_stock = p_inter * current_stock
d_stock = current_stock - i_stock

contrib = 0

for year in range(0, inp("simulation_years")):
    if year > inp("halt_contributions_after_year"):
        monthly_i = 0
        monthly_d = 0
        monthly_b = 0

    for month in range(0, 12):
        i_stock = i_stock + i_stock * f_stock_yield + monthly_i
        d_stock = d_stock + d_stock * d_stock_yield + monthly_d
        current_bond = current_bond + current_bond * bond_yield + monthly_b
        contrib += monthly_i + monthly_d + monthly_b
        tot = i_stock + d_stock + current_bond
        print("year: {}, month: {}, total: ${:,.2f}, bond %: {:.2f}, stock %: {:.2f} ({:.2f}% domestic, {:.2f}% international)".format(year + 1, month + 1, tot, 100 * (current_bond / tot), 100 * ((i_stock + d_stock) / tot), 100 * (d_stock / (i_stock + d_stock)), 100 * (i_stock / (i_stock + d_stock))))


print("\nYears simulated: {}, Resulting savings: ${:,.2f}".format(inp("simulation_years"), tot))
print("\nTotal contributions: ${:,}, Interest earned: ${:,.2f}".format(contrib, tot - (portfolio + contrib)))


print("\nDisclaimer: This is only a simulation! Actual market conditions will be much more volatile. Past performance is no guarantee of future performance.")
print("Disclaimer: This simulation assumes that you own funds that broadly track market indices. If you try to pick individual stocks, your variance from this result will be even greater.")
print("\nHint: Try playing around with the expected returns for domestic and international investments.")
print("Hint: Also, try setting halt_contributions_after_year to something lower (and witness the magic of compound interest).")
