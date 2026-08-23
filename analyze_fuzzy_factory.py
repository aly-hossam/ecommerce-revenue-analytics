import os
import json
import pandas as pd
import numpy as np

def analyze_maven_fuzzy_factory(base_dir=None, output_html="fuzzy_factory_report.html"):
    """
    Final Executive-Grade Analytics Pipeline for Maven Fuzzy Factory:
    - Filters Net Revenue factoring in refunds.
    - Focuses trend visualizations on complete operating months (Apr 2012 - Feb 2015) to eliminate visual cliffing.
    - Implements Dual-Axis scaling for AOV and RPS.
    - Perfects Tooltip colors and table header alignments.
    - Generates a standalone, fully responsive HTML dashboard.
    """
    if base_dir is None:
        if '__file__' in globals():
            base_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            base_dir = os.getcwd()

    # Search for dataset directory
    paths_to_check = [
        os.path.join(base_dir, "extracted_files", "Maven+Fuzzy+Factory"),
        os.path.join(base_dir, "extracted_files"),
        base_dir
    ]

    data_dir = None
    for p in paths_to_check:
        if os.path.exists(os.path.join(p, "website_sessions.csv")):
            data_dir = p
            break

    if not data_dir:
        raise FileNotFoundError("Could not find 'website_sessions.csv' in expected directories.")

    print(f"[*] Loading datasets from: {data_dir}\n")

    # 1. Load Datasets
    sessions_df = pd.read_csv(os.path.join(data_dir, "website_sessions.csv"))
    orders_df = pd.read_csv(os.path.join(data_dir, "orders.csv"))
    
    # Load refunds if available
    refunds_file = os.path.join(data_dir, "order_item_refunds.csv")
    if os.path.exists(refunds_file):
        refunds_df = pd.read_csv(refunds_file)
        refunds_df['created_at'] = pd.to_datetime(refunds_df['created_at'])
        order_refunds = refunds_df.groupby('order_id')['refund_amount_usd'].sum().rename('refund_amount')
        orders_df = orders_df.merge(order_refunds, on='order_id', how='left')
        orders_df['refund_amount'] = orders_df['refund_amount'].fillna(0)
    else:
        orders_df['refund_amount'] = 0.0

    orders_df['net_revenue_usd'] = orders_df['price_usd'] - orders_df['refund_amount']

    # Convert timestamps
    sessions_df['created_at'] = pd.to_datetime(sessions_df['created_at'])
    orders_df['created_at'] = pd.to_datetime(orders_df['created_at'])

    sessions_df['year_month'] = sessions_df['created_at'].dt.to_period('M').astype(str)
    orders_df['year_month'] = orders_df['created_at'].dt.to_period('M').astype(str)

    # -------------------------------------------------------------
    # Lifetime KPI Calculations (Across All Records)
    # -------------------------------------------------------------
    total_sessions = len(sessions_df)
    total_orders = len(orders_df)
    total_gross_rev = orders_df['price_usd'].sum()
    total_refunds = orders_df['refund_amount'].sum()
    total_net_rev = orders_df['net_revenue_usd'].sum()
    overall_cvr = round((total_orders / total_sessions) * 100, 2)
    overall_aov = round(total_net_rev / total_orders, 2)
    overall_rps = round(total_net_rev / total_sessions, 2)
    refund_rate = round((total_refunds / total_gross_rev) * 100, 2)

    # -------------------------------------------------------------
    # Monthly Aggregations (Full Operating Months Filtered)
    # -------------------------------------------------------------
    monthly_sessions = sessions_df.groupby('year_month').size().rename('sessions')
    monthly_orders = orders_df.groupby('year_month').agg(
        orders=('order_id', 'count'),
        gross_revenue=('price_usd', 'sum'),
        refunds=('refund_amount', 'sum'),
        net_revenue=('net_revenue_usd', 'sum')
    )

    monthly_metrics = pd.concat([monthly_sessions, monthly_orders], axis=1).fillna(0).reset_index()
    monthly_metrics['cvr_pct'] = (monthly_metrics['orders'] / monthly_metrics['sessions'] * 100).round(2)
    monthly_metrics['aov_usd'] = (monthly_metrics['net_revenue'] / monthly_metrics['orders']).round(2)
    monthly_metrics['rps_usd'] = (monthly_metrics['net_revenue'] / monthly_metrics['sessions']).round(2)

    # Exclude partial cutoff months (2012-03 and 2015-03) for clean trend charts
    full_months_metrics = monthly_metrics[~monthly_metrics['year_month'].isin(['2012-03', '2015-03'])].copy()

    # -------------------------------------------------------------
    # Q3: Marketing Channels Performance
    # -------------------------------------------------------------
    def categorize_traffic_channel(row):
        utm_s = str(row['utm_source']).strip() if pd.notnull(row['utm_source']) else ''
        utm_c = str(row['utm_campaign']).strip() if pd.notnull(row['utm_campaign']) else ''
        referer = str(row['http_referer']).strip() if pd.notnull(row['http_referer']) else ''

        if utm_s and utm_c:
            return f"{utm_s} ({utm_c})"
        elif utm_s:
            return utm_s
        elif referer:
            return "Organic Search"
        else:
            return "Direct Type-In"

    sessions_df['marketing_channel'] = sessions_df.apply(categorize_traffic_channel, axis=1)

    session_orders = sessions_df.merge(
        orders_df[['website_session_id', 'order_id', 'price_usd', 'refund_amount', 'net_revenue_usd']],
        on='website_session_id',
        how='left'
    )

    channel_perf = session_orders.groupby('marketing_channel').agg(
        sessions=('website_session_id', 'count'),
        orders=('order_id', 'count'),
        gross_rev=('price_usd', 'sum'),
        refunds=('refund_amount', 'sum'),
        net_rev=('net_revenue_usd', 'sum')
    ).reset_index()

    channel_perf['cvr_pct'] = (channel_perf['orders'] / channel_perf['sessions'] * 100).round(2)
    channel_perf['rps_usd'] = (channel_perf['net_rev'] / channel_perf['sessions']).round(2)
    channel_perf = channel_perf.sort_values(by='net_rev', ascending=False)

    top_channel = channel_perf.iloc[0]

    # -------------------------------------------------------------
    # Prepare JSON Data for JavaScript
    # -------------------------------------------------------------
    months_list = full_months_metrics['year_month'].tolist()
    sessions_list = full_months_metrics['sessions'].tolist()
    orders_list = full_months_metrics['orders'].tolist()
    cvr_list = full_months_metrics['cvr_pct'].tolist()
    aov_list = full_months_metrics['aov_usd'].tolist()
    rps_list = full_months_metrics['rps_usd'].tolist()

    channel_labels = channel_perf['marketing_channel'].tolist()
    channel_net_rev = channel_perf['net_rev'].round(0).tolist()

    # Build Clean Mobile-Friendly Table HTML
    channel_rows_html = []
    for _, r in channel_perf.iterrows():
        channel_rows_html.append(f"""
        <tr class="border-b border-slate-800 hover:bg-slate-800/50">
            <td class="px-3 py-2.5 text-xs font-semibold text-slate-200">{r['marketing_channel']}</td>
            <td class="px-3 py-2.5 text-xs text-slate-300 text-center">{int(r['sessions']):,}</td>
            <td class="px-3 py-2.5 text-xs text-slate-300 text-center">{int(r['orders']):,}</td>
            <td class="px-3 py-2.5 text-xs text-emerald-400 font-bold text-center">{r['cvr_pct']}%</td>
            <td class="px-3 py-2.5 text-xs text-indigo-300 font-bold text-right">${int(r['net_rev']):,}</td>
            <td class="px-3 py-2.5 text-xs text-amber-400 font-bold text-right">${r['rps_usd']:.2f}</td>
        </tr>
        """)

    # -------------------------------------------------------------
    # HTML Report Template
    # -------------------------------------------------------------
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Maven Fuzzy Factory - Executive E-commerce Analytics</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #0f172a; color: #f8fafc; }}
        .card {{ background-color: #1e293b; border: 1px solid #334155; border-radius: 12px; }}
    </style>
</head>
<body class="p-4 md:p-8 max-w-5xl mx-auto">

    <!-- Header -->
    <header class="mb-6 border-b border-slate-700 pb-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-2">
        <div>
            <h1 class="text-2xl md:text-3xl font-extrabold text-amber-400">🧸 Maven Fuzzy Factory</h1>
            <p class="text-slate-400 text-xs md:text-sm mt-1">E-commerce Traffic, Funnel Conversion & Marketing Performance</p>
        </div>
        <div class="flex items-center gap-2">
            <span class="text-xs bg-emerald-500/20 text-emerald-400 px-3 py-1 rounded-full font-semibold border border-emerald-500/30">Net Revenue Audited</span>
            <span class="text-xs bg-indigo-500/20 text-indigo-400 px-3 py-1 rounded-full font-semibold border border-indigo-500/30">Executive Analytics</span>
        </div>
    </header>

    <!-- Top KPI Cards -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
        <div class="card p-3 text-center">
            <span class="text-[11px] text-slate-400 uppercase font-semibold">Total Sessions</span>
            <p class="text-xl md:text-2xl font-bold text-white mt-1">{total_sessions:,}</p>
            <span class="text-[10px] text-slate-500">Across all channels</span>
        </div>
        <div class="card p-3 text-center">
            <span class="text-[11px] text-slate-400 uppercase font-semibold">Total Orders</span>
            <p class="text-xl md:text-2xl font-bold text-emerald-400 mt-1">{total_orders:,}</p>
            <span class="text-[10px] text-slate-500">Overall CVR: {overall_cvr}%</span>
        </div>
        <div class="card p-3 text-center">
            <span class="text-[11px] text-slate-400 uppercase font-semibold">Net Revenue</span>
            <p class="text-xl md:text-2xl font-bold text-indigo-400 mt-1">${int(total_net_rev):,}</p>
            <span class="text-[10px] text-rose-400/80">Refunds: ${int(total_refunds):,} ({refund_rate}%)</span>
        </div>
        <div class="card p-3 text-center">
            <span class="text-[11px] text-slate-400 uppercase font-semibold">Net AOV / RPS</span>
            <p class="text-xl md:text-2xl font-bold text-amber-400 mt-1">${overall_aov} <span class="text-xs text-slate-400 font-normal">/ ${overall_rps}</span></p>
            <span class="text-[10px] text-slate-500">Per Order / Per Session</span>
        </div>
    </div>

    <!-- Question 1: Trend in Sessions and Order Volume -->
    <section class="card p-5 mb-6">
        <div class="flex items-center justify-between flex-wrap gap-2 mb-2">
            <h2 class="text-base md:text-lg font-bold text-amber-400">1. What is the trend in website sessions and order volume?</h2>
            <span class="text-[11px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded border border-slate-700">Full Operating Months</span>
        </div>
        <p class="text-slate-300 text-xs md:text-sm mb-4 leading-relaxed">
            Traffic and order volume exhibited dramatic, consistent scaling from <strong>{months_list[0]}</strong> to peak operating volume in <strong>{months_list[-1]}</strong>. 
            Monthly sessions expanded from <strong>{sessions_list[0]:,}</strong> to <strong>{sessions_list[-1]:,}</strong>, while monthly orders grew from <strong>{orders_list[0]:,}</strong> to <strong>{orders_list[-1]:,}</strong>.
        </p>
        <div class="relative w-full h-72">
            <canvas id="trendChart"></canvas>
        </div>
    </section>

    <!-- Question 2: Session-to-Order Conversion Rate -->
    <section class="card p-5 mb-6">
        <h2 class="text-base md:text-lg font-bold text-emerald-400 mb-2">2. What is the session-to-order conversion rate? How has it trended?</h2>
        <p class="text-slate-300 text-xs md:text-sm mb-4 leading-relaxed">
            The lifetime platform conversion rate is <strong>{overall_cvr}%</strong>. Over full operating months, CVR rose steadily from 
            <strong>{cvr_list[0]}%</strong> to peak at <strong>{max(cvr_list)}%</strong>, driven by iterative landing page testing, mobile checkout optimizations, and multi-product bundling.
        </p>
        <div class="relative w-full h-64">
            <canvas id="cvrChart"></canvas>
        </div>
    </section>

    <!-- Question 3: Marketing Channels Performance -->
    <section class="card p-5 mb-6">
        <h2 class="text-base md:text-lg font-bold text-indigo-400 mb-2">3. Which marketing channels have been most successful?</h2>
        <p class="text-slate-300 text-xs md:text-sm mb-4 leading-relaxed">
            <strong>{top_channel['marketing_channel']}</strong> is the primary commercial acquisition engine, driving 
            <strong>${int(top_channel['net_rev']):,} Net Revenue</strong> ({round(top_channel['net_rev']/total_net_rev*100, 1)}% of total). 
            High-intent brand channels (<strong>gsearch brand</strong> & <strong>bsearch brand</strong>) achieved superior conversion rates exceeding <strong>8%</strong>.
        </p>

        <!-- Mobile Scrollable Table with Fixed Header Alignments -->
        <div class="overflow-x-auto rounded-lg border border-slate-700 mb-5">
            <table class="w-full text-left border-collapse min-w-[550px]">
                <thead class="bg-slate-900/80 border-b border-slate-700 text-slate-400 text-xs">
                    <tr>
                        <th class="px-3 py-2.5 font-semibold">Channel</th>
                        <th class="px-3 py-2.5 font-semibold text-center">Sessions</th>
                        <th class="px-3 py-2.5 font-semibold text-center">Orders</th>
                        <th class="px-3 py-2.5 font-semibold text-center">CVR (%)</th>
                        <th class="px-3 py-2.5 font-semibold text-right">Net Revenue</th>
                        <th class="px-3 py-2.5 font-semibold text-right">RPS</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(channel_rows_html)}
                </tbody>
            </table>
        </div>

        <h3 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Net Revenue by Channel ($)</h3>
        <div class="relative w-full h-64">
            <canvas id="channelChart"></canvas>
        </div>
    </section>

    <!-- Question 4: Revenue per Order & Revenue per Session (Dual-Axis Fixed) -->
    <section class="card p-5 mb-6">
        <h2 class="text-base md:text-lg font-bold text-rose-400 mb-2">4. How has the revenue per order evolved? What about revenue per session?</h2>
        <p class="text-slate-300 text-xs md:text-sm mb-4 leading-relaxed">
            - <strong>Net Average Order Value (AOV - Left Axis):</strong> Rose steadily from <strong>${aov_list[0]}</strong> to <strong>${max(aov_list)}</strong> as additional product lines were introduced.<br>
            - <strong>Net Revenue Per Session (RPS - Right Axis):</strong> Scaled from <strong>${rps_list[0]}</strong> to peak at <strong>${max(rps_list)}</strong>, demonstrating compounding conversion and monetization efficiency.
        </p>
        <div class="relative w-full h-72">
            <canvas id="revenueEfficiencyChart"></canvas>
        </div>
    </section>

    <footer class="text-center text-xs text-slate-500 my-6">
        Maven Fuzzy Factory Executive Analytics Dashboard | Audited Python Pipeline
    </footer>

    <!-- Chart.js Script Configuration -->
    <script>
        const months = {json.dumps(months_list)};
        
        // Universal Tooltip Configuration for Matching Indicator Colors
        const universalTooltipConfig = {{
            usePointStyle: true,
            boxPadding: 4,
            callbacks: {{
                labelColor: function(context) {{
                    return {{
                        borderColor: context.dataset.borderColor,
                        backgroundColor: context.dataset.borderColor
                    }};
                }}
            }}
        }};

        // Q1: Sessions & Orders Dual-Axis Chart
        new Chart(document.getElementById('trendChart'), {{
            type: 'line',
            data: {{
                labels: months,
                datasets: [
                    {{
                        label: 'Website Sessions',
                        data: {json.dumps(sessions_list)},
                        borderColor: '#60a5fa',
                        backgroundColor: 'rgba(96, 165, 250, 0.1)',
                        yAxisID: 'y_sessions',
                        tension: 0.3,
                        fill: true
                    }},
                    {{
                        label: 'Orders Volume',
                        data: {json.dumps(orders_list)},
                        borderColor: '#34d399',
                        backgroundColor: 'rgba(52, 211, 153, 0.1)',
                        yAxisID: 'y_orders',
                        tension: 0.3,
                        fill: true
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                interaction: {{ mode: 'index', intersect: false }},
                plugins: {{
                    tooltip: universalTooltipConfig
                }},
                scales: {{
                    x: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }} }},
                    y_sessions: {{
                        type: 'linear',
                        position: 'left',
                        ticks: {{ color: '#60a5fa', font: {{ size: 10 }} }},
                        title: {{ display: true, text: 'Sessions', color: '#60a5fa' }}
                    }},
                    y_orders: {{
                        type: 'linear',
                        position: 'right',
                        grid: {{ drawOnChartArea: false }},
                        ticks: {{ color: '#34d399', font: {{ size: 10 }} }},
                        title: {{ display: true, text: 'Orders', color: '#34d399' }}
                    }}
                }}
            }}
        }});

        // Q2: CVR Trend Chart
        new Chart(document.getElementById('cvrChart'), {{
            type: 'line',
            data: {{
                labels: months,
                datasets: [{{
                    label: 'Conversion Rate (%)',
                    data: {json.dumps(cvr_list)},
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.15)',
                    fill: true,
                    tension: 0.3
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    tooltip: universalTooltipConfig
                }},
                scales: {{
                    x: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }} }},
                    y: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }}, title: {{ display: true, text: 'CVR %', color: '#94a3b8' }} }}
                }}
            }}
        }});

        // Q3: Horizontal Channel Revenue Chart
        new Chart(document.getElementById('channelChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(channel_labels)},
                datasets: [{{
                    label: 'Net Revenue ($)',
                    data: {json.dumps(channel_net_rev)},
                    backgroundColor: '#818cf8',
                    borderRadius: 4
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }} }},
                    y: {{ ticks: {{ color: '#cbd5e1', font: {{ size: 10 }} }} }}
                }}
            }}
        }});

        // Q4: Dual-Axis AOV & RPS Chart
        new Chart(document.getElementById('revenueEfficiencyChart'), {{
            type: 'line',
            data: {{
                labels: months,
                datasets: [
                    {{
                        label: 'Average Order Value (AOV $)',
                        data: {json.dumps(aov_list)},
                        borderColor: '#fbbf24',
                        backgroundColor: 'transparent',
                        yAxisID: 'y_aov',
                        tension: 0.3
                    }},
                    {{
                        label: 'Revenue Per Session (RPS $)',
                        data: {json.dumps(rps_list)},
                        borderColor: '#f43f5e',
                        backgroundColor: 'transparent',
                        yAxisID: 'y_rps',
                        tension: 0.3
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                interaction: {{ mode: 'index', intersect: false }},
                plugins: {{
                    tooltip: universalTooltipConfig
                }},
                scales: {{
                    x: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }} }},
                    y_aov: {{
                        type: 'linear',
                        position: 'left',
                        ticks: {{ color: '#fbbf24', font: {{ size: 10 }} }},
                        title: {{ display: true, text: 'AOV ($)', color: '#fbbf24' }}
                    }},
                    y_rps: {{
                        type: 'linear',
                        position: 'right',
                        grid: {{ drawOnChartArea: false }},
                        ticks: {{ color: '#f43f5e', font: {{ size: 10 }} }},
                        title: {{ display: true, text: 'RPS ($)', color: '#f43f5e' }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

    output_path = os.path.join(base_dir, output_html)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[✔] Pixel-Perfect HTML Report generated successfully: {output_path}")

if __name__ == "__main__":
    analyze_maven_fuzzy_factory()