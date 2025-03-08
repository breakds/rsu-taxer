import numpy as np

from pnl_analyzer.protocols import PlotData, PlotLayout, PlotResponse


SHORT_TERM_RATE = 0.51
LONG_TERM_RATE = 0.35
ORDINARY_RATE = 0.51


def calculate_pnl_curves(settlement_price: float, num_shares: int, long_term_capital_gain: float, short_term_capital_gain: float) -> PlotResponse:
    sell_prices = np.arange(0.0, settlement_price * 1.2, 0.1)

    # TODO(breakds): Precise withhold tax rate
    withhold = settlement_price * num_shares * 0.5
    sold = sell_prices * num_shares

    # Part I: net cashflow
    net_cashflow = sold - withhold

    # Part II: tax save
    tax_save = np.zeros_like(sold)
    capital_loss = np.where(sold < withhold, withhold - sold, 0.0)

    # Save on Ordinary Income
    deductible = np.where(capital_loss > 3000.0, 3000.0, capital_loss)
    tax_save += deductible * ORDINARY_RATE
    capital_loss -= deductible

    # Save on short term capital gain
    deductible= np.where(capital_loss > short_term_capital_gain,
                         short_term_capital_gain,
                         capital_loss)
    tax_save += deductible * SHORT_TERM_RATE
    capital_loss -= deductible

    # Save on long term capital_loss
    deductible= np.where(capital_loss > long_term_capital_gain,
                         long_term_capital_gain,
                         capital_loss)
    tax_save += deductible * LONG_TERM_RATE
    capital_loss -= deductible

    # Create the net cashflow curve
    net_cashflow_curve = PlotData(
        x=sell_prices.tolist(),
        y=net_cashflow.tolist(),
        type="scatter",
        mode="line",
        stackgroup="pnl",
        fill="tonexty",
        name="Net Cashflow")
    tax_save_curve = PlotData(
        x=sell_prices.tolist(),
        y=tax_save.tolist(),
        type="scatter",
        mode="line",
        stackgroup="pnl",
        fill="tonexty",
        name="Tax Save")
    cash_curve = PlotData(
        x=sell_prices.tolist(),
        y=tax_save.tolist(),
        type="scatter",
        mode="line",
        marker={"color": "red"},
        name="Tax Save")

    return PlotResponse(
        data=[net_cashflow_curve, tax_save_curve, cash_curve],
        layout=PlotLayout(
            title={"text": "收益损失曲线"},
            xaxis={"title": "解禁后出售价格"},
            yaxis={"title": "金额($)"}),
    )
