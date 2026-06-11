"""Generate the complete Project 4 data-visualization submission."""

from __future__ import annotations

import argparse
import base64
import html
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter


PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = PROJECT_DIR / "Dataset for Data Analytics.xlsx"
DEFAULT_OUTPUT = PROJECT_DIR / "outputs"

NAVY = "#12304A"
BLUE = "#1479B8"
LIGHT_BLUE = "#A9D5EC"
ORANGE = "#EF7D32"
RED = "#C94747"
GREEN = "#23856D"
GREY = "#AAB4BE"
LIGHT_GREY = "#E8EDF1"
DARK_GREY = "#4D5963"
WHITE = "#FFFFFF"

EXPECTED_COLUMNS = {
    "OrderID",
    "Date",
    "CustomerID",
    "Product",
    "Quantity",
    "UnitPrice",
    "ShippingAddress",
    "PaymentMethod",
    "OrderStatus",
    "TrackingNumber",
    "ItemsInCart",
    "CouponCode",
    "ReferralSource",
    "TotalPrice",
}


def currency(value: float) -> str:
    """Format a numeric value as compact currency."""
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if abs(value) >= 100_000:
        return f"${value / 1_000:.0f}K"
    return f"${value:,.0f}"


def currency_axis(value: float, _position: int) -> str:
    return currency(value)


def configure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 16,
            "axes.titleweight": "bold",
            "axes.labelcolor": DARK_GREY,
            "axes.edgecolor": LIGHT_GREY,
            "xtick.color": DARK_GREY,
            "ytick.color": DARK_GREY,
            "figure.facecolor": WHITE,
            "axes.facecolor": WHITE,
            "savefig.facecolor": WHITE,
        }
    )


def load_and_validate(path: Path) -> pd.DataFrame:
    """Load, standardize, and validate the source workbook."""
    if not path.exists():
        raise FileNotFoundError(f"Input workbook not found: {path}")

    df = pd.read_excel(path)
    missing_columns = EXPECTED_COLUMNS.difference(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")
    if df.empty:
        raise ValueError("The dataset contains no rows.")

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="raise")
    for column in ("Quantity", "UnitPrice", "ItemsInCart", "TotalPrice"):
        df[column] = pd.to_numeric(df[column], errors="raise")

    if df["OrderID"].duplicated().any():
        raise ValueError("OrderID must be unique.")
    if df["OrderID"].isna().any() or df["Date"].isna().any():
        raise ValueError("OrderID and Date cannot be null.")
    if (df[["Quantity", "UnitPrice", "ItemsInCart", "TotalPrice"]] < 0).any().any():
        raise ValueError("Numeric order fields cannot contain negative values.")

    expected_total = (df["Quantity"] * df["UnitPrice"]).round(2)
    if not expected_total.eq(df["TotalPrice"].round(2)).all():
        raise ValueError("TotalPrice does not consistently equal Quantity x UnitPrice.")

    df["CouponCode"] = df["CouponCode"].fillna("NO_COUPON")
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp()
    df["IsIssue"] = df["OrderStatus"].isin(["Cancelled", "Returned"])
    return df


def build_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    monthly = (
        df.groupby("Month")
        .agg(GrossOrderValue=("TotalPrice", "sum"), Orders=("OrderID", "count"))
        .reset_index()
    )
    monthly["AverageOrderValue"] = monthly["GrossOrderValue"] / monthly["Orders"]

    h1 = (
        df[df["Date"].dt.month <= 6]
        .groupby("Year")
        .agg(
            GrossOrderValue=("TotalPrice", "sum"),
            Orders=("OrderID", "count"),
            AverageOrderValue=("TotalPrice", "mean"),
            IssueRate=("IsIssue", "mean"),
        )
        .reset_index()
    )

    product = (
        df.groupby("Product")
        .agg(
            GrossOrderValue=("TotalPrice", "sum"),
            Orders=("OrderID", "count"),
            Units=("Quantity", "sum"),
            AverageOrderValue=("TotalPrice", "mean"),
            IssueRate=("IsIssue", "mean"),
        )
        .sort_values("GrossOrderValue")
        .reset_index()
    )

    status = (
        df.groupby("OrderStatus")
        .agg(GrossOrderValue=("TotalPrice", "sum"), Orders=("OrderID", "count"))
        .reset_index()
    )
    status["OrderShare"] = status["Orders"] / len(df)
    status_order = ["Delivered", "Shipped", "Pending", "Returned", "Cancelled"]
    status["OrderStatus"] = pd.Categorical(
        status["OrderStatus"], categories=status_order, ordered=True
    )
    status = status.sort_values("OrderStatus").reset_index(drop=True)

    referral = (
        df.groupby("ReferralSource")
        .agg(
            GrossOrderValue=("TotalPrice", "sum"),
            Orders=("OrderID", "count"),
            AverageOrderValue=("TotalPrice", "mean"),
            IssueRate=("IsIssue", "mean"),
        )
        .sort_values("GrossOrderValue")
        .reset_index()
    )

    coupon = (
        df.groupby("CouponCode")
        .agg(
            GrossOrderValue=("TotalPrice", "sum"),
            Orders=("OrderID", "count"),
            AverageOrderValue=("TotalPrice", "mean"),
            IssueRate=("IsIssue", "mean"),
        )
        .sort_values("AverageOrderValue")
        .reset_index()
    )

    return {
        "monthly": monthly,
        "h1": h1,
        "product": product,
        "status": status,
        "referral": referral,
        "coupon": coupon,
    }


def save_figure(fig: plt.Figure, path: Path) -> None:
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def add_source(fig: plt.Figure, text: str = "Source: Dataset for Data Analytics.xlsx") -> None:
    fig.text(0.01, 0.01, text, fontsize=8, color=DARK_GREY)


def chart_h1_trend(h1: pd.DataFrame, output: Path) -> Path:
    path = output / "01_h1_gross_order_value.png"
    fig, ax = plt.subplots(figsize=(11, 6))
    values = h1["GrossOrderValue"]
    ax.plot(h1["Year"], values, color=BLUE, marker="o", linewidth=3, markersize=9)
    ax.fill_between(h1["Year"], values, alpha=0.08, color=BLUE)
    ax.set_title(
        "H1 gross order value fell 19% from 2023 to 2025",
        loc="left",
        color=NAVY,
        pad=18,
    )
    ax.set_ylabel("Gross order value")
    ax.set_xlabel("")
    ax.set_xticks(h1["Year"])
    ax.yaxis.set_major_formatter(FuncFormatter(currency_axis))
    ax.grid(axis="y", color=LIGHT_GREY, linewidth=0.8)
    ax.grid(axis="x", visible=False)
    ax.spines[["top", "right"]].set_visible(False)
    for year, value in zip(h1["Year"], values):
        ax.annotate(
            currency(value),
            (year, value),
            xytext=(0, 12),
            textcoords="offset points",
            ha="center",
            fontweight="bold",
            color=NAVY,
        )
    add_source(fig, "Source: Dataset for Data Analytics.xlsx | H1 (Jan-Jun) comparison")
    save_figure(fig, path)
    return path


def chart_product(product: pd.DataFrame, output: Path) -> Path:
    path = output / "02_product_performance.png"
    fig, ax = plt.subplots(figsize=(11, 6))
    leader = product["GrossOrderValue"].idxmax()
    colors = [BLUE if index == leader else LIGHT_BLUE for index in product.index]
    bars = ax.barh(product["Product"], product["GrossOrderValue"], color=colors)
    ax.set_title(
        "Chair and Printer are virtually tied for product leadership",
        loc="left",
        color=NAVY,
        pad=18,
    )
    ax.set_xlabel("Gross order value")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(FuncFormatter(currency_axis))
    ax.grid(axis="x", color=LIGHT_GREY, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.bar_label(bars, labels=[currency(v) for v in product["GrossOrderValue"]], padding=5)
    add_source(fig)
    save_figure(fig, path)
    return path


def chart_status(status: pd.DataFrame, output: Path) -> Path:
    path = output / "03_order_status_distribution.png"
    fig, ax = plt.subplots(figsize=(11, 6))
    colors = [
        RED if value in {"Cancelled", "Returned"} else GREY
        for value in status["OrderStatus"].astype(str)
    ]
    bars = ax.barh(status["OrderStatus"].astype(str), status["OrderShare"] * 100, color=colors)
    issue_share = status.loc[
        status["OrderStatus"].astype(str).isin(["Cancelled", "Returned"]), "OrderShare"
    ].sum()
    ax.set_title(
        f"Cancelled and returned orders account for {issue_share:.1%} of volume",
        loc="left",
        color=NAVY,
        pad=18,
    )
    ax.set_xlabel("Share of orders")
    ax.set_ylabel("")
    ax.set_xlim(0, max(status["OrderShare"] * 100) + 5)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _pos: f"{value:.0f}%"))
    ax.grid(axis="x", color=LIGHT_GREY, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.bar_label(
        bars,
        labels=[f"{value:.1%}" for value in status["OrderShare"]],
        padding=5,
    )
    add_source(fig)
    save_figure(fig, path)
    return path


def chart_referral(referral: pd.DataFrame, output: Path) -> Path:
    path = output / "04_referral_source_performance.png"
    fig, ax = plt.subplots(figsize=(11, 6))
    best = referral["GrossOrderValue"].idxmax()
    colors = [GREEN if index == best else LIGHT_BLUE for index in referral.index]
    bars = ax.barh(referral["ReferralSource"], referral["GrossOrderValue"], color=colors)
    instagram = referral.loc[referral["ReferralSource"] == "Instagram"].iloc[0]
    ax.set_title(
        f"Instagram leads acquisition and has the lowest issue rate ({instagram['IssueRate']:.1%})",
        loc="left",
        color=NAVY,
        pad=18,
    )
    ax.set_xlabel("Gross order value")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(FuncFormatter(currency_axis))
    ax.grid(axis="x", color=LIGHT_GREY, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    labels = [
        f"{currency(value)} | {rate:.1%} issue"
        for value, rate in zip(referral["GrossOrderValue"], referral["IssueRate"])
    ]
    ax.bar_label(bars, labels=labels, padding=5, fontsize=9)
    add_source(fig)
    save_figure(fig, path)
    return path


def chart_coupon(coupon: pd.DataFrame, output: Path) -> Path:
    path = output / "05_coupon_average_order_value.png"
    fig, ax = plt.subplots(figsize=(11, 6))
    colors = [ORANGE if value == "FREESHIP" else GREY for value in coupon["CouponCode"]]
    bars = ax.barh(coupon["CouponCode"], coupon["AverageOrderValue"], color=colors)
    spread = coupon["AverageOrderValue"].max() - coupon["AverageOrderValue"].min()
    ax.set_title(
        f"Coupon choice shifts average order value by only {currency(spread)}",
        loc="left",
        color=NAVY,
        pad=18,
    )
    ax.set_xlabel("Average order value")
    ax.set_ylabel("")
    ax.set_xlim(0, coupon["AverageOrderValue"].max() * 1.15)
    ax.xaxis.set_major_formatter(FuncFormatter(currency_axis))
    ax.grid(axis="x", color=LIGHT_GREY, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.bar_label(
        bars,
        labels=[currency(value) for value in coupon["AverageOrderValue"]],
        padding=5,
    )
    add_source(fig)
    save_figure(fig, path)
    return path


def chart_executive_dashboard(
    df: pd.DataFrame, tables: dict[str, pd.DataFrame], output: Path
) -> Path:
    path = output / "00_executive_dashboard.png"
    fig = plt.figure(figsize=(16, 9))
    grid = fig.add_gridspec(3, 12, height_ratios=[0.7, 1.35, 1.35], hspace=0.8, wspace=1.2)
    fig.suptitle(
        "Revenue momentum is weakening while order outcomes remain the main risk",
        x=0.04,
        y=0.97,
        ha="left",
        fontsize=23,
        fontweight="bold",
        color=NAVY,
    )
    fig.text(
        0.04,
        0.92,
        "Executive view | 1,200 e-commerce orders | January 2023 to June 2025",
        fontsize=11,
        color=DARK_GREY,
    )

    total = df["TotalPrice"].sum()
    aov = df["TotalPrice"].mean()
    issue_rate = df["IsIssue"].mean()
    h1 = tables["h1"]
    h1_change = (
        h1.loc[h1["Year"] == 2025, "GrossOrderValue"].iloc[0]
        / h1.loc[h1["Year"] == 2023, "GrossOrderValue"].iloc[0]
        - 1
    )
    kpis = [
        ("GROSS ORDER VALUE", currency(total), "All recorded orders", BLUE),
        ("AVERAGE ORDER VALUE", currency(aov), "Across 1,200 orders", NAVY),
        ("CANCEL + RETURN RATE", f"{issue_rate:.1%}", "Primary operational risk", RED),
        ("H1 2025 VS H1 2023", f"{h1_change:.1%}", "Comparable-period decline", ORANGE),
    ]
    for index, (label, value, note, color) in enumerate(kpis):
        ax = fig.add_subplot(grid[0, index * 3 : (index + 1) * 3])
        ax.axis("off")
        ax.text(0, 0.84, label, fontsize=9, fontweight="bold", color=DARK_GREY)
        ax.text(0, 0.38, value, fontsize=24, fontweight="bold", color=color)
        ax.text(0, 0.06, note, fontsize=9, color=DARK_GREY)

    ax1 = fig.add_subplot(grid[1:, :5])
    product = tables["product"]
    top_index = product["GrossOrderValue"].idxmax()
    colors = [BLUE if index == top_index else LIGHT_BLUE for index in product.index]
    bars = ax1.barh(product["Product"], product["GrossOrderValue"], color=colors)
    ax1.set_title("Product value is broadly diversified", loc="left", color=NAVY)
    ax1.xaxis.set_major_formatter(FuncFormatter(currency_axis))
    ax1.grid(axis="x", color=LIGHT_GREY)
    ax1.set_axisbelow(True)
    ax1.spines[["top", "right", "left"]].set_visible(False)
    ax1.tick_params(axis="y", length=0)
    ax1.bar_label(bars, labels=[currency(v) for v in product["GrossOrderValue"]], padding=4, fontsize=8)

    ax2 = fig.add_subplot(grid[1, 6:])
    h1_values = tables["h1"]
    ax2.plot(
        h1_values["Year"],
        h1_values["GrossOrderValue"],
        color=BLUE,
        marker="o",
        linewidth=3,
    )
    ax2.set_title("Comparable H1 value declined each year", loc="left", color=NAVY)
    ax2.set_xticks(h1_values["Year"])
    ax2.yaxis.set_major_formatter(FuncFormatter(currency_axis))
    ax2.grid(axis="y", color=LIGHT_GREY)
    ax2.spines[["top", "right"]].set_visible(False)
    for year, value in zip(h1_values["Year"], h1_values["GrossOrderValue"]):
        ax2.annotate(currency(value), (year, value), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=9)

    ax3 = fig.add_subplot(grid[2, 6:])
    status = tables["status"]
    status_colors = [
        RED if value in {"Cancelled", "Returned"} else GREY
        for value in status["OrderStatus"].astype(str)
    ]
    bars = ax3.barh(status["OrderStatus"].astype(str), status["OrderShare"] * 100, color=status_colors)
    ax3.set_title("Two in five orders are cancelled or returned", loc="left", color=NAVY)
    ax3.xaxis.set_major_formatter(FuncFormatter(lambda value, _pos: f"{value:.0f}%"))
    ax3.grid(axis="x", color=LIGHT_GREY)
    ax3.set_axisbelow(True)
    ax3.spines[["top", "right", "left"]].set_visible(False)
    ax3.tick_params(axis="y", length=0)
    ax3.bar_label(bars, labels=[f"{v:.1%}" for v in status["OrderShare"]], padding=4, fontsize=8)

    fig.text(
        0.04,
        0.02,
        "Recommendation: diagnose cancellation and return drivers first, then protect Instagram acquisition while testing offers by incremental margin.",
        fontsize=10,
        fontweight="bold",
        color=NAVY,
    )
    save_figure(fig, path)
    return path


def build_summary(df: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    h1 = tables["h1"].set_index("Year")
    referral = tables["referral"].sort_values("GrossOrderValue", ascending=False)
    product = tables["product"].sort_values("GrossOrderValue", ascending=False)
    coupon = tables["coupon"].sort_values("AverageOrderValue", ascending=False)
    metrics = [
        ("Orders", len(df), "count"),
        ("Gross order value", df["TotalPrice"].sum(), "currency"),
        ("Average order value", df["TotalPrice"].mean(), "currency"),
        ("Cancel + return rate", df["IsIssue"].mean(), "percentage"),
        ("Delivered order rate", (df["OrderStatus"] == "Delivered").mean(), "percentage"),
        ("H1 2025 vs H1 2023 gross value", h1.loc[2025, "GrossOrderValue"] / h1.loc[2023, "GrossOrderValue"] - 1, "percentage"),
        ("Top product", product.iloc[0]["Product"], "text"),
        ("Top referral source", referral.iloc[0]["ReferralSource"], "text"),
        ("Lowest referral issue rate", referral.sort_values("IssueRate").iloc[0]["ReferralSource"], "text"),
        ("Highest coupon AOV", coupon.iloc[0]["CouponCode"], "text"),
    ]
    return pd.DataFrame(metrics, columns=["Metric", "Value", "Format"])


def image_data_uri(path: Path) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def build_html_report(
    df: pd.DataFrame,
    tables: dict[str, pd.DataFrame],
    charts: list[Path],
    output: Path,
) -> Path:
    path = output / "executive_report.html"
    h1 = tables["h1"].set_index("Year")
    h1_decline = h1.loc[2025, "GrossOrderValue"] / h1.loc[2023, "GrossOrderValue"] - 1
    issue_rate = df["IsIssue"].mean()
    referral = tables["referral"].sort_values("GrossOrderValue", ascending=False).iloc[0]
    coupon = tables["coupon"]
    coupon_spread = coupon["AverageOrderValue"].max() - coupon["AverageOrderValue"].min()

    cards = [
        ("Gross order value", currency(df["TotalPrice"].sum())),
        ("Average order value", currency(df["TotalPrice"].mean())),
        ("Cancel + return rate", f"{issue_rate:.1%}"),
        ("H1 2025 vs H1 2023", f"{h1_decline:.1%}"),
    ]
    card_html = "".join(
        f'<div class="card"><span>{html.escape(label)}</span><strong>{html.escape(value)}</strong></div>'
        for label, value in cards
    )
    chart_html = "".join(
        f'<section class="chart"><img src="{image_data_uri(chart)}" alt="{html.escape(chart.stem)}"></section>'
        for chart in charts
    )

    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Project 4 Executive Data Story</title>
  <style>
    :root {{ --navy:#12304A; --blue:#1479B8; --red:#C94747; --ink:#2E3A43; --muted:#667580; --line:#E2E8ED; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: #F4F7F9; color: var(--ink); font-family: Arial, sans-serif; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 48px 28px 72px; }}
    header {{ background: var(--navy); color: white; padding: 42px; border-radius: 12px; }}
    h1 {{ margin: 0 0 12px; max-width: 900px; font-size: 38px; line-height: 1.15; }}
    header p {{ margin: 0; color: #D7E6F0; }}
    .cards {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 24px 0; }}
    .card {{ background: white; border: 1px solid var(--line); padding: 20px; border-radius: 10px; }}
    .card span {{ display: block; color: var(--muted); font-size: 13px; text-transform: uppercase; }}
    .card strong {{ display: block; color: var(--navy); font-size: 28px; margin-top: 8px; }}
    .story {{ background: white; padding: 30px; border-left: 6px solid var(--blue); border-radius: 8px; margin-bottom: 24px; }}
    .story h2, .actions h2 {{ color: var(--navy); margin-top: 0; }}
    li {{ margin: 10px 0; line-height: 1.5; }}
    .chart {{ background: white; border: 1px solid var(--line); border-radius: 10px; padding: 16px; margin: 18px 0; }}
    .chart img {{ display: block; width: 100%; height: auto; }}
    .actions {{ background: #EAF4F9; padding: 30px; border-radius: 10px; margin-top: 24px; }}
    footer {{ color: var(--muted); margin-top: 28px; font-size: 13px; }}
    @media (max-width: 800px) {{ .cards {{ grid-template-columns: repeat(2, 1fr); }} h1 {{ font-size: 30px; }} }}
  </style>
</head>
<body>
<main>
  <header>
    <h1>Revenue momentum is weakening while order outcomes remain the main risk</h1>
    <p>DecodeLabs Project 4 | Executive data visualization | January 2023 to June 2025</p>
  </header>
  <div class="cards">{card_html}</div>
  <section class="story">
    <h2>What the data says</h2>
    <ul>
      <li>Comparable H1 gross order value declined {abs(h1_decline):.1%} from 2023 to 2025.</li>
      <li>Cancelled and returned orders represent {issue_rate:.1%} of all recorded orders.</li>
      <li>{html.escape(str(referral['ReferralSource']))} leads with {currency(referral['GrossOrderValue'])} in gross value and a {referral['IssueRate']:.1%} issue rate.</li>
      <li>Coupon-level average order value spans only {currency(coupon_spread)}, so offer selection alone is unlikely to reverse the trend.</li>
    </ul>
  </section>
  {chart_html}
  <section class="actions">
    <h2>Recommended action</h2>
    <ol>
      <li>Investigate cancellation and return causes by product and acquisition source before increasing demand spend.</li>
      <li>Protect and scale Instagram acquisition while monitoring whether its lower issue rate persists.</li>
      <li>Evaluate promotions on incremental profit and completed-order conversion, not gross order value alone.</li>
      <li>Track H1 and monthly cohorts consistently; do not compare partial 2025 with full prior years.</li>
    </ol>
  </section>
  <footer>Gross order value includes all statuses and should not be interpreted as recognized revenue. Generated reproducibly by data_visualization.py.</footer>
</main>
</body>
</html>"""
    path.write_text(document, encoding="utf-8")
    return path


def export_outputs(
    df: pd.DataFrame, tables: dict[str, pd.DataFrame], output: Path
) -> list[Path]:
    output.mkdir(parents=True, exist_ok=True)
    cleaned_path = output / "analysis_ready_orders.csv"
    df.drop(columns=["IsIssue"]).to_csv(cleaned_path, index=False, date_format="%Y-%m-%d")

    summary = build_summary(df, tables)
    summary_path = output / "key_metrics.csv"
    summary.to_csv(summary_path, index=False)

    for name, table in tables.items():
        table.to_csv(output / f"table_{name}.csv", index=False)

    charts = [
        chart_executive_dashboard(df, tables, output),
        chart_h1_trend(tables["h1"], output),
        chart_product(tables["product"], output),
        chart_status(tables["status"], output),
        chart_referral(tables["referral"], output),
        chart_coupon(tables["coupon"], output),
    ]
    report = build_html_report(df, tables, charts, output)
    return [cleaned_path, summary_path, *charts, report]


def run(input_path: Path = DEFAULT_INPUT, output_dir: Path = DEFAULT_OUTPUT) -> list[Path]:
    configure_style()
    df = load_and_validate(input_path)
    tables = build_tables(df)
    return export_outputs(df, tables, output_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Project 4 visualizations and executive report."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Path to the source Excel workbook.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Directory for generated outputs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generated = run(args.input.resolve(), args.output.resolve())
    print(f"Validated and analyzed: {args.input.resolve()}")
    print("Generated:")
    for path in generated:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
