import pandas as pd
import requests
import os

def download_data(url, output_path):
    print(f"Downloading data from {url}...")
    # OneDrive direct download link transformation
    download_url = url.replace("1drv.ms/x/c/", "1drv.ms/u/c/").split("?")[0] + "?download=1"
    
    # Try the provided URL as is first if it looks like a sharing link
    if "1drv.ms" in url:
        # One way to get direct link from short link
        response = requests.get(url, allow_redirects=True)
        final_url = response.url.replace("redir?", "download?").replace("view.aspx", "download.aspx")
    
    r = requests.get(url, allow_redirects=True)
    with open(output_path, 'wb') as f:
        f.write(r.content)
    print(f"File saved to {output_path}")

def convert_to_csv(excel_path, csv_path):
    print(f"Converting {excel_path} to {csv_path}...")
    # Check if the file is actually an Excel file (sometimes downloads are HTML if auth fails)
    try:
        df = pd.read_excel(excel_path)
        # Add an 'id' column if it doesn't exist, as the project expects it
        if 'id' not in df.columns:
            df.insert(0, 'id', range(1, len(df) + 1))
        
        df.to_csv(csv_path, index=False)
        print(f"Successfully converted to {csv_path}")
        return True
    except Exception as e:
        print(f"Error converting file: {e}")
        # If it failed, maybe it's the synthetic data generation fallback or wait for user
        return False

if __name__ == "__main__":
    onedrive_url = "https://1drv.ms/x/c/8ee8877b2329f038/IQD1i2iwvBTbQ4ae1YTcVe14AdJqLTNNznM-k_1Iq6ViGhA?e=PdF4Rv"
    excel_file = "dataset/housing_data_new.xlsx"
    csv_file = "dataset/housing_data.csv"
    
    os.makedirs("dataset", exist_ok=True)
    
    # In a real scenario, downloading from OneDrive short links via scripts can be tricky without the direct link.
    # Since I have browser access, I'll try to use the browser to get it if this fails.
    # But let's try the request first.
    download_data(onedrive_url, excel_file)
    if convert_to_csv(excel_file, csv_file):
        print("Data update complete.")
    else:
        print("Data update failed. Check if the download link is valid or if the file is accessible.")
