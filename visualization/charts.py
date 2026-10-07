import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class ProductVisualizer:
    """Clean scraped product data and generate portfolio-ready charts."""

    def __init__(self, file_path, output_dir="outputs"):
        self.file_path = file_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.df = pd.read_csv(file_path)
        print("\nDataset loaded successfully!")
        print(f"Rows: {len(self.df)}")
        print(f"Columns: {len(self.df.columns)}")

    def _save_plot(self, filename):
        path = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"Saved: {path}")

    def clean_price(self):
        self.df["Price"] = (
            self.df["Price"]
            .astype(str)
            .str.extract(r"(\d[\d,]*)", expand=False)
            .str.replace(",", "", regex=False)
        )
        self.df["Price"] = pd.to_numeric(self.df["Price"], errors="coerce")

        if "Rating" in self.df.columns:
            self.df["Rating"] = pd.to_numeric(
                self.df["Rating"], errors="coerce"
            )

        self.df.dropna(subset=["Price"], inplace=True)
        self.df = self.df[self.df["Price"] >= 0].copy()

        print("Price cleaning completed.")
        print(f"Usable rows: {len(self.df)}")

    def numpy_analysis(self):
        prices = self.df["Price"].to_numpy()

        if len(prices) == 0:
            print("No valid prices available.")
            return

        print("\nNumPy Statistical Analysis")
        print(f"Mean Price: ₹{np.mean(prices):,.2f}")
        print(f"Median Price: ₹{np.median(prices):,.2f}")
        print(f"Maximum Price: ₹{np.max(prices):,.2f}")
        print(f"Minimum Price: ₹{np.min(prices):,.2f}")
        print(f"Standard Deviation: ₹{np.std(prices):,.2f}")

    def price_distribution(self):
        plt.figure(figsize=(10, 5))
        sns.histplot(self.df["Price"], bins=20, kde=True)
        plt.title("Price Distribution")
        plt.xlabel("Price (₹)")
        plt.ylabel("Number of Products")
        self._save_plot("price_distribution.png")

    def box_plot(self):
        plt.figure(figsize=(8, 5))
        sns.boxplot(x=self.df["Price"])
        plt.title("Price Distribution - Box Plot")
        plt.xlabel("Price (₹)")
        self._save_plot("price_boxplot.png")

    def kde_plot(self):
        plt.figure(figsize=(8, 5))
        sns.kdeplot(self.df["Price"], fill=True)
        plt.title("Price Density")
        plt.xlabel("Price (₹)")
        self._save_plot("price_kde.png")

    def violin_plot(self):
        plt.figure(figsize=(8, 5))
        sns.violinplot(x=self.df["Price"])
        plt.title("Price Distribution - Violin Plot")
        plt.xlabel("Price (₹)")
        self._save_plot("price_violin.png")

    def top_expensive_products(self):
        top_products = (
            self.df.nlargest(10, "Price")
            .sort_values("Price")
        )

        plt.figure(figsize=(12, 6))
        sns.barplot(
            data=top_products,
            x="Price",
            y="Product Name",
        )
        plt.title("Top 10 Most Expensive Products")
        plt.xlabel("Price (₹)")
        plt.ylabel("Product")
        self._save_plot("top_10_expensive_products.png")

    def scatter_plot(self):
        if "Rating" not in self.df.columns:
            print("Rating column not available.")
            return

        ratings_df = self.df.dropna(subset=["Rating"])

        if ratings_df.empty:
            print("No valid ratings available.")
            return

        plt.figure(figsize=(8, 5))
        sns.scatterplot(
            data=ratings_df,
            x="Rating",
            y="Price",
        )
        plt.title("Rating vs Price")
        plt.xlabel("Rating")
        plt.ylabel("Price (₹)")
        self._save_plot("rating_vs_price.png")

    def heatmap(self):
        numeric_df = self.df.select_dtypes(include=np.number)

        if numeric_df.shape[1] < 2:
            print("Not enough numeric columns for correlation heatmap.")
            return

        plt.figure(figsize=(8, 5))
        sns.heatmap(
            numeric_df.corr(),
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
        )
        plt.title("Numeric Feature Correlation")
        self._save_plot("correlation_heatmap.png")

    def count_plot(self):
        if "Brand" not in self.df.columns:
            print("Brand column not available.")
            return

        top_brands = self.df["Brand"].value_counts().head(10)

        plt.figure(figsize=(10, 6))
        sns.barplot(
            x=top_brands.values,
            y=top_brands.index,
        )
        plt.title("Top 10 Brands by Product Count")
        plt.xlabel("Number of Products")
        plt.ylabel("Brand")
        self._save_plot("top_brands.png")

    def pie_chart(self):
        if "Brand" not in self.df.columns:
            print("Brand column not available.")
            return

        top_brands = self.df["Brand"].value_counts().head(5)

        plt.figure(figsize=(7, 7))
        plt.pie(
            top_brands.values,
            labels=top_brands.index,
            autopct="%1.1f%%",
        )
        plt.title("Top 5 Brands by Product Count")
        self._save_plot("top_5_brands.png")

    def ratings_analysis(self):
        if "Rating" not in self.df.columns:
            print("Rating column not available.")
            return

        ratings_df = self.df.dropna(subset=["Rating"])

        if ratings_df.empty:
            print("No valid ratings available.")
            return

        plt.figure(figsize=(8, 5))
        sns.boxplot(x=ratings_df["Rating"])
        plt.title("Product Ratings Distribution")
        plt.xlabel("Rating")
        self._save_plot("ratings_distribution.png")
