from src.data_collection import collect_samsung_tweets, test_api_access

def main():
    print("Testing API access...")
    test_api_access()
    
    print("\nStarting Samsung tweet collection...")
    df = collect_samsung_tweets()
    if df is not None:
        print(f"Collected {len(df)} tweets")
    else:
        print("Failed to collect tweets")

if __name__ == "__main__":
    main()