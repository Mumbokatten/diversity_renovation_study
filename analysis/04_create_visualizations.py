"""
Create Visualizations for Diversity and Renovation Study
=========================================================
This script creates publication-quality maps and graphs for the research paper.

Visualizations include:
- Maps: Permit distribution, diversity indices across Sweden
- Scatter plots: Diversity vs. renovation patterns
- Histograms: Distribution of key variables
- Correlation heatmaps

All outputs saved as high-resolution PNG files suitable for academic papers.

References:
-----------
Tufte, E. R. (2001). The visual display of quantitative information (2nd ed.).
    Graphics Press.

Wilke, C. O. (2019). Fundamentals of data visualization. O'Reilly Media.
    https://clauswilke.com/dataviz/
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

# Set style for publication-quality figures
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

# File paths
INPUT_FILE = "analysis/diversity_indices.csv"
OUTPUT_DIR = "analysis/figures"

def plot_diversity_distribution(df):
    """
    Plot distribution of diversity indices.

    Creates histogram and density plots for Simpson, Shannon, and foreign-born %.

    Args:
        df: DataFrame with diversity indices

    Returns:
        str: Path to saved figure
    """
    print("\nCreating diversity distribution plots...")

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Simpson Index
    if 'simpson_index' in df.columns:
        axes[0].hist(df['simpson_index'].dropna(), bins=30, color='steelblue',
                     edgecolor='black', alpha=0.7)
        axes[0].axvline(df['simpson_index'].median(), color='red', linestyle='--',
                       linewidth=2, label=f'Median: {df["simpson_index"].median():.3f}')
        axes[0].set_xlabel('Simpson Diversity Index')
        axes[0].set_ylabel('Frequency')
        axes[0].set_title('(A) Simpson Index Distribution')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

    # Shannon Index
    if 'shannon_index' in df.columns:
        axes[1].hist(df['shannon_index'].dropna(), bins=30, color='darkorange',
                     edgecolor='black', alpha=0.7)
        axes[1].axvline(df['shannon_index'].median(), color='red', linestyle='--',
                       linewidth=2, label=f'Median: {df["shannon_index"].median():.3f}')
        axes[1].set_xlabel('Shannon Entropy Index')
        axes[1].set_ylabel('Frequency')
        axes[1].set_title('(B) Shannon Index Distribution')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

    # Foreign-born percentage
    if 'foreign_born_pct' in df.columns:
        axes[2].hist(df['foreign_born_pct'].dropna() * 100, bins=30, color='forestgreen',
                     edgecolor='black', alpha=0.7)
        axes[2].axvline(df['foreign_born_pct'].median() * 100, color='red', linestyle='--',
                       linewidth=2, label=f'Median: {df["foreign_born_pct"].median()*100:.1f}%')
        axes[2].set_xlabel('Foreign-born Population (%)')
        axes[2].set_ylabel('Frequency')
        axes[2].set_title('(C) Foreign-born % Distribution')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = f"{OUTPUT_DIR}/diversity_distributions.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"  ✓ Saved: {output_path}")
    return output_path

def plot_geographic_map(df):
    """
    Create map of permit locations across Sweden.

    Color-coded by diversity index (if available) or municipality.

    Args:
        df: DataFrame with coordinates and diversity data

    Returns:
        str: Path to saved figure
    """
    print("\nCreating geographic map...")

    # Check if we have coordinates
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        print("  ⚠ WARNING: No coordinate data available")
        return None

    fig, axes = plt.subplots(1, 2, figsize=(14, 10))

    # Map 1: All permits
    ax1 = axes[0]
    scatter1 = ax1.scatter(df['longitude'], df['latitude'], c='steelblue',
                          alpha=0.5, s=10, edgecolors='none')
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.set_title('(A) Building Permits Across Sweden\n(Past 30 Months)')
    ax1.grid(True, alpha=0.3)

    # Add approximate Sweden boundaries for context
    ax1.set_xlim(10, 25)
    ax1.set_ylim(55, 70)

    # Map 2: Colored by diversity
    ax2 = axes[1]
    if 'simpson_index' in df.columns:
        scatter2 = ax2.scatter(df['longitude'], df['latitude'],
                              c=df['simpson_index'], cmap='RdYlGn',
                              alpha=0.6, s=15, edgecolors='black', linewidth=0.5)
        cbar = plt.colorbar(scatter2, ax=ax2)
        cbar.set_label('Simpson Diversity Index\n(Green = More Diverse)', rotation=270,
                      labelpad=20)
        ax2.set_title('(B) Permits Colored by\nNeighborhood Diversity')
    else:
        ax2.scatter(df['longitude'], df['latitude'], c='coral',
                   alpha=0.5, s=10, edgecolors='none')
        ax2.set_title('(B) Building Permits\n(Diversity data pending)')

    ax2.set_xlabel('Longitude')
    ax2.set_ylabel('Latitude')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(10, 25)
    ax2.set_ylim(55, 70)

    plt.tight_layout()
    output_path = f"{OUTPUT_DIR}/geographic_map.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"  ✓ Saved: {output_path}")
    return output_path

def plot_permits_by_municipality(df):
    """
    Bar chart showing top municipalities by permit count.

    Args:
        df: DataFrame with municipality information

    Returns:
        str: Path to saved figure
    """
    print("\nCreating municipality comparison chart...")

    if 'municipality' not in df.columns:
        print("  ⚠ WARNING: No municipality data available")
        return None

    # Count permits by municipality
    muni_counts = df['municipality'].value_counts().head(20)

    fig, ax = plt.subplots(figsize=(12, 8))

    bars = ax.barh(range(len(muni_counts)), muni_counts.values, color='steelblue',
                   edgecolor='black', alpha=0.8)

    # Color Stockholm differently
    for i, muni in enumerate(muni_counts.index):
        if 'Stockholm' in muni:
            bars[i].set_color('crimson')

    ax.set_yticks(range(len(muni_counts)))
    ax.set_yticklabels(muni_counts.index)
    ax.set_xlabel('Number of Building Permits (Past 30 Months)')
    ax.set_title('Top 20 Municipalities by Permit Count', fontsize=14, fontweight='bold')
    ax.grid(True, axis='x', alpha=0.3)

    # Add legend
    blue_patch = mpatches.Patch(color='steelblue', label='Other municipalities')
    red_patch = mpatches.Patch(color='crimson', label='Stockholm region')
    ax.legend(handles=[blue_patch, red_patch], loc='lower right')

    # Add value labels on bars
    for i, v in enumerate(muni_counts.values):
        ax.text(v + 5, i, str(v), va='center', fontweight='bold')

    plt.tight_layout()
    output_path = f"{OUTPUT_DIR}/permits_by_municipality.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"  ✓ Saved: {output_path}")
    return output_path

def plot_diversity_vs_population(df):
    """
    Scatter plot: Diversity indices vs. population.

    Shows relationship between neighborhood size and diversity.

    Args:
        df: DataFrame with diversity and population data

    Returns:
        str: Path to saved figure
    """
    print("\nCreating diversity vs. population scatter plots...")

    # Check data availability
    has_simpson = 'simpson_index' in df.columns
    has_shannon = 'shannon_index' in df.columns
    has_population = any('population' in col.lower() for col in df.columns)

    if not (has_simpson or has_shannon) or not has_population:
        print("  ⚠ WARNING: Missing required data for scatter plots")
        return None

    # Get population column
    pop_cols = [col for col in df.columns if 'population' in col.lower()]
    if pop_cols:
        pop_col = pop_cols[0]
    else:
        return None

    # Create figure
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Simpson vs Population
    if has_simpson:
        ax1 = axes[0]
        ax1.scatter(df[pop_col], df['simpson_index'], alpha=0.5, s=20,
                   color='steelblue', edgecolors='black', linewidth=0.5)
        ax1.set_xlabel('Total Population')
        ax1.set_ylabel('Simpson Diversity Index')
        ax1.set_title('(A) Diversity vs. Population Size')
        ax1.grid(True, alpha=0.3)

        # Add trend line
        valid_data = df[[pop_col, 'simpson_index']].dropna()
        if len(valid_data) > 10:
            z = np.polyfit(valid_data[pop_col], valid_data['simpson_index'], 1)
            p = np.poly1d(z)
            x_trend = np.linspace(valid_data[pop_col].min(), valid_data[pop_col].max(), 100)
            ax1.plot(x_trend, p(x_trend), "r--", alpha=0.8, linewidth=2,
                    label='Linear trend')
            ax1.legend()

    # Shannon vs Population
    if has_shannon:
        ax2 = axes[1]
        ax2.scatter(df[pop_col], df['shannon_index'], alpha=0.5, s=20,
                   color='darkorange', edgecolors='black', linewidth=0.5)
        ax2.set_xlabel('Total Population')
        ax2.set_ylabel('Shannon Entropy Index')
        ax2.set_title('(B) Shannon Index vs. Population Size')
        ax2.grid(True, alpha=0.3)

        # Add trend line
        valid_data = df[[pop_col, 'shannon_index']].dropna()
        if len(valid_data) > 10:
            z = np.polyfit(valid_data[pop_col], valid_data['shannon_index'], 1)
            p = np.poly1d(z)
            x_trend = np.linspace(valid_data[pop_col].min(), valid_data[pop_col].max(), 100)
            ax2.plot(x_trend, p(x_trend), "r--", alpha=0.8, linewidth=2,
                    label='Linear trend')
            ax2.legend()

    plt.tight_layout()
    output_path = f"{OUTPUT_DIR}/diversity_vs_population.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"  ✓ Saved: {output_path}")
    return output_path

def plot_correlation_heatmap(df):
    """
    Correlation heatmap for key variables.

    Args:
        df: DataFrame with all variables

    Returns:
        str: Path to saved figure
    """
    print("\nCreating correlation heatmap...")

    # Select numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    # Select key variables
    key_vars = []
    for col in ['simpson_index', 'shannon_index', 'fractionalization', 'foreign_born_pct']:
        if col in numeric_cols:
            key_vars.append(col)

    # Add any population, income, education variables
    for col in numeric_cols:
        if any(keyword in col.lower() for keyword in ['population', 'income', 'education', 'tenure']):
            if col not in key_vars:
                key_vars.append(col)

    if len(key_vars) < 2:
        print("  ⚠ WARNING: Not enough variables for correlation heatmap")
        return None

    # Calculate correlation matrix
    corr_matrix = df[key_vars].corr()

    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))

    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                vmin=-1, vmax=1, ax=ax)

    ax.set_title('Correlation Matrix: Key Variables', fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    output_path = f"{OUTPUT_DIR}/correlation_heatmap.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"  ✓ Saved: {output_path}")
    return output_path

def plot_permit_timeline(df):
    """
    Timeline showing permits over time.

    Args:
        df: DataFrame with publication_date

    Returns:
        str: Path to saved figure
    """
    print("\nCreating permit timeline...")

    if 'publication_date' not in df.columns:
        print("  ⚠ WARNING: No publication_date column")
        return None

    # Convert to datetime
    df_time = df.copy()
    df_time['publication_date'] = pd.to_datetime(df_time['publication_date'], errors='coerce')

    # Group by month
    df_time['year_month'] = df_time['publication_date'].dt.to_period('M')
    monthly_counts = df_time.groupby('year_month').size()

    fig, ax = plt.subplots(figsize=(14, 5))

    # Convert period to timestamp for plotting
    x_dates = [period.to_timestamp() for period in monthly_counts.index]
    ax.plot(x_dates, monthly_counts.values, marker='o', linewidth=2,
            markersize=5, color='steelblue')

    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Permits Published')
    ax.set_title('Building Permits Over Time', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    output_path = f"{OUTPUT_DIR}/permit_timeline.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"  ✓ Saved: {output_path}")
    return output_path

def create_summary_figure(df):
    """
    Create comprehensive summary figure with multiple panels.

    Args:
        df: DataFrame with all data

    Returns:
        str: Path to saved figure
    """
    print("\nCreating summary figure...")

    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

    # Panel A: Map
    ax1 = fig.add_subplot(gs[0:2, 0:2])
    if 'latitude' in df.columns and 'longitude' in df.columns:
        if 'simpson_index' in df.columns:
            scatter = ax1.scatter(df['longitude'], df['latitude'],
                                c=df['simpson_index'], cmap='RdYlGn',
                                alpha=0.6, s=15, edgecolors='black', linewidth=0.5)
            cbar = plt.colorbar(scatter, ax=ax1)
            cbar.set_label('Simpson Index', rotation=270, labelpad=15)
        else:
            ax1.scatter(df['longitude'], df['latitude'], c='steelblue',
                       alpha=0.5, s=10, edgecolors='none')
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.set_title('(A) Geographic Distribution', fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # Panel B: Diversity distribution
    ax2 = fig.add_subplot(gs[0, 2])
    if 'simpson_index' in df.columns:
        ax2.hist(df['simpson_index'].dropna(), bins=20, color='steelblue',
                edgecolor='black', alpha=0.7)
        ax2.set_xlabel('Simpson Index')
        ax2.set_ylabel('Frequency')
        ax2.set_title('(B) Diversity\nDistribution', fontweight='bold')
        ax2.grid(True, alpha=0.3)

    # Panel C: Foreign-born %
    ax3 = fig.add_subplot(gs[1, 2])
    if 'foreign_born_pct' in df.columns:
        ax3.hist(df['foreign_born_pct'].dropna() * 100, bins=20,
                color='forestgreen', edgecolor='black', alpha=0.7)
        ax3.set_xlabel('Foreign-born %')
        ax3.set_ylabel('Frequency')
        ax3.set_title('(C) Foreign-born\n%', fontweight='bold')
        ax3.grid(True, alpha=0.3)

    # Panel D: Top municipalities
    ax4 = fig.add_subplot(gs[2, :])
    if 'municipality' in df.columns:
        muni_counts = df['municipality'].value_counts().head(10)
        bars = ax4.barh(range(len(muni_counts)), muni_counts.values,
                       color='steelblue', edgecolor='black', alpha=0.8)
        ax4.set_yticks(range(len(muni_counts)))
        ax4.set_yticklabels(muni_counts.index, fontsize=8)
        ax4.set_xlabel('Number of Permits')
        ax4.set_title('(D) Top 10 Municipalities', fontweight='bold')
        ax4.grid(True, axis='x', alpha=0.3)

    plt.suptitle('Diversity and Renovation Study: Data Overview',
                fontsize=16, fontweight='bold', y=0.995)

    output_path = f"{OUTPUT_DIR}/summary_figure.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"  ✓ Saved: {output_path}")
    return output_path

def main():
    """
    Main execution: Create all visualizations.
    """
    print("=" * 60)
    print("Creating Visualizations")
    print("=" * 60)

    # Load data
    print(f"\nLoading data from {INPUT_FILE}...")

    if not Path(INPUT_FILE).exists():
        print(f"\nERROR: {INPUT_FILE} not found!")
        print("Please run 01_calculate_diversity_indices.py first.")
        return

    df = pd.read_csv(INPUT_FILE)
    print(f"Data loaded: {len(df)} observations")

    # Create output directory
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # Create all visualizations
    figures_created = []

    # 1. Diversity distributions
    fig_path = plot_diversity_distribution(df)
    if fig_path:
        figures_created.append(fig_path)

    # 2. Geographic map
    fig_path = plot_geographic_map(df)
    if fig_path:
        figures_created.append(fig_path)

    # 3. Municipalities
    fig_path = plot_permits_by_municipality(df)
    if fig_path:
        figures_created.append(fig_path)

    # 4. Diversity vs population
    fig_path = plot_diversity_vs_population(df)
    if fig_path:
        figures_created.append(fig_path)

    # 5. Correlation heatmap
    fig_path = plot_correlation_heatmap(df)
    if fig_path:
        figures_created.append(fig_path)

    # 6. Timeline
    fig_path = plot_permit_timeline(df)
    if fig_path:
        figures_created.append(fig_path)

    # 7. Summary figure (comprehensive)
    fig_path = create_summary_figure(df)
    if fig_path:
        figures_created.append(fig_path)

    # Summary
    print("\n" + "=" * 60)
    print("VISUALIZATION COMPLETE")
    print("=" * 60)
    print(f"\n✓ Created {len(figures_created)} figures")
    print(f"✓ Saved to: {OUTPUT_DIR}/")
    print("\nFigures created:")
    for fig in figures_created:
        print(f"  - {Path(fig).name}")

    print("\n" + "=" * 60)
    print("Notes on Visualizations")
    print("=" * 60)
    print("- All figures are 300 DPI (publication quality)")
    print("- Maps show approximate Sweden boundaries")
    print("- Color schemes: Green = high diversity, Red = low diversity")
    print("- All figures include legends and axis labels")
    print("- Ready for inclusion in research paper")

if __name__ == "__main__":
    main()
