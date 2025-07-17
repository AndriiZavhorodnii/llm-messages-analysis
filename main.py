#!/usr/bin/env python3
"""
Review Analysis: Trustpilot vs App Store
========================================

This script analyzes customer reviews from both Trustpilot and App Store 
to understand customer sentiment, feedback patterns, and insights.

Datasets:
- Trustpilot Reviews: data/Headway_Appstore_metrics - Trustpilot_reviews.csv
- App Store Reviews: data/Headway_Appstore_metrics - AppStore_reviews.csv
"""

# =============================================================================
# CELL 1: Import Libraries and Setup
# =============================================================================
print("=" * 60)
print("CELL 1: Import Libraries and Setup")
print("=" * 60)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import os
import sys
import re
from collections import Counter

# Suppress warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)

print("Libraries imported successfully!")
print(f"Pandas version: {pd.__version__}")
print(f"NumPy version: {np.__version__}")
print(f"Matplotlib version: {plt.matplotlib.__version__}")
print(f"Seaborn version: {sns.__version__}")

# =============================================================================
# CELL 2: Load and Explore Trustpilot Data
# =============================================================================
print("\n" + "=" * 60)
print("CELL 2: Load and Explore Trustpilot Data")
print("=" * 60)

# Check if file exists
trustpilot_file = 'data/Headway_Appstore_metrics - Trustpilot_reviews.csv'
if not os.path.exists(trustpilot_file):
    print(f"Error: {trustpilot_file} not found!")
    sys.exit(1)

# Load Trustpilot reviews
try:
    trustpilot_df = pd.read_csv(trustpilot_file)
    print("✅ Trustpilot data loaded successfully!")
except Exception as e:
    print(f"Error loading Trustpilot data: {e}")
    sys.exit(1)

print("\n=== TRUSTPILOT DATASET OVERVIEW ===")
print(f"Shape: {trustpilot_df.shape}")
print(f"Columns: {list(trustpilot_df.columns)}")
print("\nFirst 5 rows:")
print(trustpilot_df.head())

print("\nData types:")
print(trustpilot_df.dtypes)

print("\nMissing values:")
print(trustpilot_df.isnull().sum())

# =============================================================================
# CELL 3: Load and Explore App Store Data
# =============================================================================
print("\n" + "=" * 60)
print("CELL 3: Load and Explore App Store Data")
print("=" * 60)

# Check if file exists
appstore_file = 'data/Headway_Appstore_metrics - AppStore_reviews.csv'
if not os.path.exists(appstore_file):
    print(f"Error: {appstore_file} not found!")
    sys.exit(1)

# Load App Store reviews
try:
    appstore_df = pd.read_csv(appstore_file)
    print("✅ App Store data loaded successfully!")
except Exception as e:
    print(f"Error loading App Store data: {e}")
    sys.exit(1)

print("\n=== APP STORE DATASET OVERVIEW ===")
print(f"Shape: {appstore_df.shape}")
print(f"Columns: {list(appstore_df.columns)}")
print("\nFirst 5 rows:")
print(appstore_df.head())

print("\nData types:")
print(appstore_df.dtypes)

print("\nMissing values:")
print(appstore_df.isnull().sum())

# =============================================================================
# CELL 4: Data Cleaning and Preprocessing
# =============================================================================
print("\n" + "=" * 60)
print("CELL 4: Data Cleaning and Preprocessing")
print("=" * 60)

def clean_dates(df, date_column):
    """Convert date column to datetime format"""
    try:
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        print(f"✅ Converted {date_column} to datetime")
        return df
    except Exception as e:
        print(f"❌ Could not convert {date_column} to datetime: {e}")
        return df

def extract_rating(rating_text):
    """Extract numeric rating from text"""
    if pd.isna(rating_text):
        return None
    try:
        import re
        numbers = re.findall(r'\d+', str(rating_text))
        if numbers:
            return int(numbers[0])
    except:
        pass
    return None

def find_rating_column(df, dataset_name):
    """Find rating column in dataset"""
    rating_columns = ['rating', 'score', 'stars', 'review_rating', 'user_rating']
    for col in rating_columns:
        if col in df.columns:
            print(f"✅ Found rating column '{col}' in {dataset_name}")
            return col
    print(f"❌ No rating column found in {dataset_name}")
    return None

def find_date_column(df, dataset_name):
    """Find date column in dataset"""
    date_columns = ['date', 'created_at', 'timestamp', 'review_date', 'submitted_at', 'published_date']
    for col in date_columns:
        if col in df.columns:
            print(f"✅ Found date column '{col}' in {dataset_name}")
            return col
    print(f"❌ No date column found in {dataset_name}")
    return None

def find_text_column(df, dataset_name):
    """Find text column in dataset"""
    text_columns = ['review', 'text', 'comment', 'content', 'message', 'review_text', 'body']
    for col in text_columns:
        if col in df.columns:
            print(f"✅ Found text column '{col}' in {dataset_name}")
            return col
    print(f"❌ No text column found in {dataset_name}")
    return None

# Find columns in both datasets
print("🔍 Identifying columns in datasets...")
trustpilot_rating_col = find_rating_column(trustpilot_df, 'Trustpilot')
trustpilot_date_col = find_date_column(trustpilot_df, 'Trustpilot')
trustpilot_text_col = find_text_column(trustpilot_df, 'Trustpilot')

appstore_rating_col = find_rating_column(appstore_df, 'App Store')
appstore_date_col = find_date_column(appstore_df, 'App Store')
appstore_text_col = find_text_column(appstore_df, 'App Store')

# Clean dates if found
if trustpilot_date_col:
    trustpilot_df = clean_dates(trustpilot_df, trustpilot_date_col)
if appstore_date_col:
    appstore_df = clean_dates(appstore_df, appstore_date_col)

print("✅ Data cleaning completed!")

# =============================================================================
# CELL 5: Basic Statistics and Summary
# =============================================================================
print("\n" + "=" * 60)
print("CELL 5: Basic Statistics and Summary")
print("=" * 60)

print("=== DATASET COMPARISON ===")
print(f"Trustpilot reviews: {len(trustpilot_df):,}")
print(f"App Store reviews: {len(appstore_df):,}")
print(f"Total reviews: {len(trustpilot_df) + len(appstore_df):,}")

print("\n=== TRUSTPILOT STATISTICS ===")
print(trustpilot_df.describe(include='all'))

print("\n=== APP STORE STATISTICS ===")
print(appstore_df.describe(include='all'))

# =============================================================================
# CELL 6: Rating Analysis and Visualization
# =============================================================================
print("\n" + "=" * 60)
print("CELL 6: Rating Analysis and Visualization")
print("=" * 60)

def plot_rating_distribution(df, rating_col, title, ax):
    """Plot rating distribution"""
    if rating_col and rating_col in df.columns:
        rating_counts = df[rating_col].value_counts().sort_index()
        ax.bar(rating_counts.index, rating_counts.values, alpha=0.7)
        ax.set_title(f'{title} - Rating Distribution')
        ax.set_xlabel('Rating')
        ax.set_ylabel('Count')
        ax.grid(True, alpha=0.3)
        
        # Add count labels on bars
        for i, v in enumerate(rating_counts.values):
            ax.text(rating_counts.index[i], v + max(rating_counts.values)*0.01, 
                   str(v), ha='center', va='bottom')
    else:
        ax.text(0.5, 0.5, f'Rating column not found\nCheck column names', 
               ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{title} - Rating Distribution')

# Create rating analysis visualizations
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Plot rating distributions
plot_rating_distribution(trustpilot_df, trustpilot_rating_col, 'Trustpilot', axes[0,0])
plot_rating_distribution(appstore_df, appstore_rating_col, 'App Store', axes[0,1])

# Average ratings comparison
avg_ratings = []
labels = []

if trustpilot_rating_col and trustpilot_rating_col in trustpilot_df.columns:
    avg_trustpilot = trustpilot_df[trustpilot_rating_col].mean()
    avg_ratings.append(avg_trustpilot)
    labels.append('Trustpilot')
    
if appstore_rating_col and appstore_rating_col in appstore_df.columns:
    avg_appstore = appstore_df[appstore_rating_col].mean()
    avg_ratings.append(avg_appstore)
    labels.append('App Store')

if avg_ratings:
    axes[1,0].bar(labels, avg_ratings, color=['skyblue', 'lightgreen'], alpha=0.7)
    axes[1,0].set_title('Average Ratings Comparison')
    axes[1,0].set_ylabel('Average Rating')
    axes[1,0].grid(True, alpha=0.3)
    
    # Add value labels on bars
    for i, v in enumerate(avg_ratings):
        axes[1,0].text(i, v + max(avg_ratings)*0.01, f'{v:.2f}', 
                      ha='center', va='bottom')

# Rating trends over time placeholder
axes[1,1].text(0.5, 0.5, 'Rating trends over time\n(if date column available)', 
               ha='center', va='center', transform=axes[1,1].transAxes)
axes[1,1].set_title('Rating Trends Over Time')

plt.tight_layout()
plt.savefig('rating_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Print summary statistics
print("\n=== RATING SUMMARY ===")
if trustpilot_rating_col and trustpilot_rating_col in trustpilot_df.columns:
    print(f"Trustpilot average rating: {trustpilot_df[trustpilot_rating_col].mean():.2f}")
    print(f"Trustpilot median rating: {trustpilot_df[trustpilot_rating_col].median():.2f}")
    print(f"Trustpilot rating std: {trustpilot_df[trustpilot_rating_col].std():.2f}")
    
if appstore_rating_col and appstore_rating_col in appstore_df.columns:
    print(f"App Store average rating: {appstore_df[appstore_rating_col].mean():.2f}")
    print(f"App Store median rating: {appstore_df[appstore_rating_col].median():.2f}")
    print(f"App Store rating std: {appstore_df[appstore_rating_col].std():.2f}")

# =============================================================================
# CELL 7: Text Analysis and Sentiment Overview
# =============================================================================
print("\n" + "=" * 60)
print("CELL 7: Text Analysis and Sentiment Overview")
print("=" * 60)

# Basic list of English stop words
STOP_WORDS = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 
    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 
    'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 
    'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 
    'weren', 'won', 'wouldn', 'app', 'headway'
]

def plot_top_words(word_counts, title, filename):
    """Plot top N most common words"""
    top_df = pd.DataFrame(word_counts, columns=['word', 'count'])
    plt.figure(figsize=(12, 8))
    sns.barplot(x='count', y='word', data=top_df, palette='viridis')
    plt.title(title)
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()

def analyze_text_column(df, text_column, dataset_name):
    """Analyze text column for basic statistics and common words"""
    if not text_column or text_column not in df.columns:
        print(f"❌ {dataset_name}: Text column '{text_column}' not found")
        return
    
    print(f"\n=== {dataset_name.upper()} TEXT ANALYSIS ===")
    
    # Remove null values
    text_data = df[text_column].dropna()
    print(f"Number of reviews with text: {len(text_data)}")
    
    if len(text_data) > 0:
        # --- Basic Stats ---
        print("\n--- Basic Statistics ---")
        word_counts = text_data.str.split().str.len()
        print(f"Average words per review: {word_counts.mean():.1f}")
        print(f"Median words per review: {word_counts.median():.1f}")
        
        char_counts = text_data.str.len()
        print(f"Average characters per review: {char_counts.mean():.1f}")
        print(f"Median characters per review: {char_counts.median():.1f}")
        
        # --- Sample Reviews ---
        print("\n--- Sample Reviews ---")
        for i, review in enumerate(text_data.head(3)):
            print(f"  {i+1}. {review[:150]}{'...' if len(review) > 150 else ''}")

        # --- Common Words and Phrases ---
        print("\n--- Common Words & Phrases ---")
        
        # Pre-process text: lowercase, remove punctuation, split into words
        words = text_data.str.lower().str.findall(r'\b\w+\b').explode()
        
        # Remove stop words
        words = words[~words.isin(STOP_WORDS)]
        
        # --- Top Unigrams (Single Words) ---
        unigram_counts = Counter(words)
        print("\nTop 15 Most Common Words:")
        for word, count in unigram_counts.most_common(15):
            print(f"  - {word}: {count:,}")
        
        # Plot top unigrams
        plot_top_words(
            unigram_counts.most_common(20),
            f'Top 20 Common Words in {dataset_name} Reviews',
            f'{dataset_name.lower().replace(" ", "_")}_common_words.png'
        )

        # --- Top Bigrams (Two-word Phrases) ---
        bigrams = list(zip(words, words.shift(-1)))
        # Remove bigrams that cross from one review to the next
        bigrams = [b for b in bigrams if not pd.isna(b[1])]
        bigram_counts = Counter(bigrams)
        print("\nTop 15 Most Common Phrases (Bigrams):")
        for (w1, w2), count in bigram_counts.most_common(15):
            print(f"  - {w1} {w2}: {count:,}")

# Analyze text columns
analyze_text_column(trustpilot_df, trustpilot_text_col, 'Trustpilot')
analyze_text_column(appstore_df, appstore_text_col, 'App Store')

# =============================================================================
# CELL 8: Time-based Analysis
# =============================================================================
print("\n" + "=" * 60)
print("CELL 8: Time-based Analysis")
print("=" * 60)

def analyze_time_trends(df, date_column, rating_column, dataset_name):
    """Analyze rating trends over time"""
    if not date_column or date_column not in df.columns:
        print(f"{dataset_name}: {date_column} column not found")
        return
    
    if not rating_column or rating_column not in df.columns:
        print(f"{dataset_name}: {rating_column} column not found")
        return
    
    # Create a copy and convert date
    temp_df = df[[date_column, rating_column]].copy()
    temp_df[date_column] = pd.to_datetime(temp_df[date_column], errors='coerce')
    temp_df = temp_df.dropna()
    
    if len(temp_df) == 0:
        print(f"{dataset_name}: No valid date data found")
        return
    
    print(f"\n=== {dataset_name.upper()} TIME ANALYSIS ===")
    print(f"Date range: {temp_df[date_column].min()} to {temp_df[date_column].max()}")
    print(f"Total days: {(temp_df[date_column].max() - temp_df[date_column].min()).days}")
    
    # Monthly average ratings
    temp_df['month'] = temp_df[date_column].dt.to_period('M')
    monthly_avg = temp_df.groupby('month')[rating_column].agg(['mean', 'count']).reset_index()
    
    # Plot monthly trends
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Average rating trend
    ax1.plot(range(len(monthly_avg)), monthly_avg['mean'], marker='o', linewidth=2)
    ax1.set_title(f'{dataset_name} - Monthly Average Ratings')
    ax1.set_ylabel('Average Rating')
    ax1.grid(True, alpha=0.3)
    
    # Review count trend
    ax2.bar(range(len(monthly_avg)), monthly_avg['count'], alpha=0.7)
    ax2.set_title(f'{dataset_name} - Monthly Review Count')
    ax2.set_ylabel('Number of Reviews')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{dataset_name.lower().replace(" ", "_")}_time_trends.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return monthly_avg

# Analyze time trends for both datasets
if trustpilot_date_col and trustpilot_rating_col:
    analyze_time_trends(trustpilot_df, trustpilot_date_col, trustpilot_rating_col, 'Trustpilot')

if appstore_date_col and appstore_rating_col:
    analyze_time_trends(appstore_df, appstore_date_col, appstore_rating_col, 'App Store')

# =============================================================================
# CELL 9: Key Insights and Summary
# =============================================================================
print("\n" + "=" * 60)
print("CELL 9: Key Insights and Summary")
print("=" * 60)

print("=== KEY INSIGHTS AND SUMMARY ===\n")

# Dataset sizes
print(f"📊 Dataset Overview:")
print(f"   • Trustpilot reviews: {len(trustpilot_df):,}")
print(f"   • App Store reviews: {len(appstore_df):,}")
print(f"   • Total reviews analyzed: {len(trustpilot_df) + len(appstore_df):,}")

# Rating comparisons
print(f"\n⭐ Rating Analysis:")
if trustpilot_rating_col and trustpilot_rating_col in trustpilot_df.columns:
    tp_avg = trustpilot_df[trustpilot_rating_col].mean()
    print(f"   • Trustpilot average: {tp_avg:.2f}/5")
    
if appstore_rating_col and appstore_rating_col in appstore_df.columns:
    as_avg = appstore_df[appstore_rating_col].mean()
    print(f"   • App Store average: {as_avg:.2f}/5")
    
    if trustpilot_rating_col and trustpilot_rating_col in trustpilot_df.columns:
        diff = abs(tp_avg - as_avg)
        print(f"   • Difference: {diff:.2f} points")
        if diff > 0.5:
            print(f"   • Significant difference detected!")

# Data quality
print(f"\n🔍 Data Quality:")
print(f"   • Trustpilot missing values: {trustpilot_df.isnull().sum().sum()}")
print(f"   • App Store missing values: {appstore_df.isnull().sum().sum()}")

# Column information
print(f"\n📋 Column Information:")
print(f"   • Trustpilot rating column: {trustpilot_rating_col or 'Not found'}")
print(f"   • Trustpilot date column: {trustpilot_date_col or 'Not found'}")
print(f"   • Trustpilot text column: {trustpilot_text_col or 'Not found'}")
print(f"   • App Store rating column: {appstore_rating_col or 'Not found'}")
print(f"   • App Store date column: {appstore_date_col or 'Not found'}")
print(f"   • App Store text column: {appstore_text_col or 'Not found'}")

# Recommendations
print(f"\n💡 Recommendations:")
print(f"   1. Review column names and adjust code accordingly")
print(f"   2. Perform sentiment analysis on review text")
print(f"   3. Identify common themes and keywords")
print(f"   4. Compare user demographics if available")
print(f"   5. Track rating trends over time")
print(f"   6. Export cleaned data for further analysis")

print(f"\n✅ Analysis completed! Check the generated plots for visual insights.")
print(f"📁 Generated files:")
print(f"   • rating_analysis.png")
if trustpilot_date_col and trustpilot_rating_col:
    print(f"   • trustpilot_time_trends.png")
if appstore_date_col and appstore_rating_col:
    print(f"   • app_store_time_trends.png")
if appstore_text_col:
    print(f"   • app_store_common_words.png")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE!")
print("=" * 60)
