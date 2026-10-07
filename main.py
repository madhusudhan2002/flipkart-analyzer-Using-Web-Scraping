from scraper.flipkart_scraper import FlipkartScraper
from visualization.charts import ProductVisualizer


def run_project():
    print("\n===================================")
    print(" Flipkart Web Scraping & EDA Project ")
    print("===================================\n")

    product = input("Enter Product Name: ").strip()
    if not product:
        print("Product name cannot be empty.")
        return

    try:
        pages = int(input("Enter Number of Pages: "))
        if pages < 1:
            raise ValueError
    except ValueError:
        print("Enter a valid positive number of pages.")
        return

    print("\nStarting Web Scraping...\n")

    scraper = FlipkartScraper(
        product_name=product,
        pages=pages,
    )
    scraper.scrape()

    df = scraper.save_data("data/flipkart_products.csv")

    if df is None:
        print("\nNo data scraped. Project stopped.")
        return

    print("\nScraping completed successfully!")
    print("\nStarting EDA & Visualization...\n")

    visualizer = ProductVisualizer(
        "data/flipkart_products.csv"
    )

    visualizer.clean_price()
    visualizer.numpy_analysis()

    print("\nGenerating visualizations...\n")
    visualizer.price_distribution()
    visualizer.box_plot()
    visualizer.kde_plot()
    visualizer.violin_plot()
    visualizer.top_expensive_products() 
    visualizer.heatmap()
    visualizer.count_plot()
    visualizer.pie_chart()

    print("\n===================================")
    print(" Project Execution Completed ")
    print("===================================\n")
    print("Cleaned dataset: data/flipkart_products.csv")
    print("Charts: outputs/")


if __name__ == "__main__":
    run_project()
