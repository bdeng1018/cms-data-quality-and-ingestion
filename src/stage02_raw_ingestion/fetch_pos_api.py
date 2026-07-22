"""
fetch_pos_api.py
Branch 1 — POS API downloader (Q2 2026 only)

Fetches the Q2 2026 Provider of Services (POS) dataset from the CMS API,
paginates through all rows, and writes the result to disk as Parquet and CSV.

Usage (from project root):

    python src/stage02_raw_ingestion/fetch_pos_api.py \
        --out-parquet data/stage02_raw/pos_q2_2026.parquet \
        --out-csv data/stage02_raw/pos_q2_2026.csv

"""

import argparse
import logging
import math
from typing import Any, Dict, List

import pandas as pd
import requests

# Q2 2026 POS dataset UUID (from CMS docs)
POS_Q2_2026_UUID = "bb342fae-b551-40fd-a738-e2e5878f3bbb"

# Base API URL (from CMS API docs)
BASE_URL = "https://data.cms.gov/data-api/v1/dataset"


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def fetch_page(uuid: str, offset: int, size: int) -> List[Dict[str, Any]]:
    """
    Fetch a single page of POS data from the CMS API.

    Parameters
    ----------
    uuid : str
        Dataset version UUID (e.g., Q2 2026).
    offset : int
        Row offset for pagination.
    size : int
        Page size (number of rows per request).

    Returns
    -------
    List[Dict[str, Any]]
        List of row dictionaries.
    """
    url = f"https://data.cms.gov/data-api/v1/dataset/{uuid}/data"
    params = {"offset": offset, "size": size}
    headers = {"Accept": "application/json"}

    logging.info("Requesting POS page: offset=%d size=%d", offset, size)
    resp = requests.get(url, params=params, headers=headers, timeout=60)

    if resp.status_code != 200:
        raise RuntimeError(f"CMS API error {resp.status_code}: {resp.text[:500]}")

    try:
        data = resp.json()
    except Exception:
        raise RuntimeError(f"CMS returned non-JSON response: {resp.text[:500]}")

    if not isinstance(data, list):
        raise ValueError(f"Unexpected response type: {type(data)}")

    logging.info("Received %d rows", len(data))
    return data


def fetch_all_pos_q2_2026(page_size: int = 5000) -> pd.DataFrame:
    """
    Fetch all Q2 2026 POS data from CMS API and return as a DataFrame.

    Parameters
    ----------
    page_size : int
        Number of rows per page (default 5000).

    Returns
    -------
    pd.DataFrame
        Combined POS dataset for Q2 2026.
    """
    # First request to determine total rows
    logging.info("Fetching initial page to determine total rows...")
    first_page = fetch_page(POS_Q2_2026_UUID, offset=0, size=page_size)
    if not first_page:
        raise RuntimeError("First page returned no data.")

    # CMS docs say Q2 2026 has 44,707 rows; we can trust that but also infer:
    total_rows = 44707
    logging.info("CMS docs report total_rows=%d for Q2 2026.", total_rows)

    pages = [first_page]
    num_pages = math.ceil(total_rows / page_size)

    logging.info("Fetching remaining %d pages...", num_pages - 1)
    for i in range(1, num_pages):
        offset = i * page_size
        page = fetch_page(POS_Q2_2026_UUID, offset=offset, size=page_size)
        pages.append(page)

    # Flatten and convert to DataFrame
    all_rows: List[Dict[str, Any]] = [row for page in pages for row in page]
    logging.info("Total combined rows: %d", len(all_rows))

    df = pd.DataFrame(all_rows)
    logging.info("Final DataFrame shape: %s", df.shape)
    return df


def main() -> None:
    configure_logging()

    parser = argparse.ArgumentParser(
        description="Fetch Q2 2026 POS dataset from CMS API and save to disk."
    )
    parser.add_argument(
        "--out-parquet",
        type=str,
        required=False,
        help="Path to write Parquet file (e.g., data/stage02_raw/pos_q2_2026.parquet).",
    )
    parser.add_argument(
        "--out-csv",
        type=str,
        required=False,
        help="Path to write CSV file (e.g., data/stage02_raw/pos_q2_2026.csv).",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=5000,
        help="Number of rows per page (default 5000).",
    )

    args = parser.parse_args()

    if not args.out_parquet and not args.out_csv:
        raise SystemExit("Must specify at least one of --out-parquet or --out-csv.")

    logging.info("Starting POS Q2 2026 fetch...")
    df = fetch_all_pos_q2_2026(page_size=args.page_size)

    if args.out_parquet:
        logging.info("Writing Parquet to %s", args.out_parquet)
        df.to_parquet(args.out_parquet, index=False)

    if args.out_csv:
        logging.info("Writing CSV to %s", args.out_csv)
        df.to_csv(args.out_csv, index=False)

    logging.info("POS Q2 2026 fetch complete.")


if __name__ == "__main__":
    main()
