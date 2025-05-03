import argparse
import logging
import whois
import datetime
import pandas as pd
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(description="Determines the age of a domain name using WHOIS lookups.")
    parser.add_argument("domain", help="The domain name to analyze (e.g., example.com)")
    parser.add_argument("-o", "--output", help="Optional output file to save results (CSV format)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    return parser.parse_args()


def analyze_domain_age(domain):
    """
    Analyzes the age of a domain name using WHOIS lookups.

    Args:
        domain (str): The domain name to analyze.

    Returns:
        dict: A dictionary containing the domain's creation date, current date, and age in days.
             Returns None if an error occurs during the WHOIS lookup.
    """
    try:
        logging.info(f"Performing WHOIS lookup for domain: {domain}")
        w = whois.whois(domain)

        if w.creation_date:
            # Handle cases where creation_date is a list or a single datetime object
            creation_date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
            current_date = datetime.datetime.now()
            age_in_days = (current_date - creation_date).days

            logging.info(f"Domain {domain} created on {creation_date}, current date is {current_date}, age is {age_in_days} days.")

            return {
                "domain": domain,
                "creation_date": creation_date,
                "current_date": current_date,
                "age_in_days": age_in_days
            }
        else:
            logging.warning(f"Could not determine creation date for domain: {domain}")
            return None
    except whois.parser.PywhoisError as e:
        logging.error(f"WHOIS lookup failed for {domain}: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during WHOIS lookup for {domain}: {e}")
        return None

def save_results_to_csv(results, output_file):
    """
    Saves the analysis results to a CSV file using pandas.

    Args:
        results (list of dict): A list of dictionaries containing the domain analysis results.
        output_file (str): The path to the output CSV file.
    """
    try:
        df = pd.DataFrame(results)
        df.to_csv(output_file, index=False)
        logging.info(f"Results saved to CSV file: {output_file}")
    except Exception as e:
        logging.error(f"Failed to save results to CSV: {e}")


def main():
    """
    Main function to execute the domain age analysis tool.
    """
    args = setup_argparse()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose logging enabled.")

    domain = args.domain

    # Input validation: Basic domain name check (more robust validation can be added)
    if not isinstance(domain, str) or not "." in domain:
        logging.error("Invalid domain name. Please provide a valid domain name (e.g., example.com).")
        sys.exit(1)


    analysis_result = analyze_domain_age(domain)

    if analysis_result:
        print(f"Domain: {analysis_result['domain']}")
        print(f"Creation Date: {analysis_result['creation_date']}")
        print(f"Current Date: {analysis_result['current_date']}")
        print(f"Age (days): {analysis_result['age_in_days']}")

        if args.output:
            save_results_to_csv([analysis_result], args.output)
    else:
        logging.warning(f"Could not retrieve domain age information for: {domain}")



if __name__ == "__main__":
    main()

# Usage Examples:

# 1. Basic usage:
# python analyze-domain-age.py example.com

# 2. With verbose logging:
# python analyze-domain-age.py example.com -v

# 3. Save results to a CSV file:
# python analyze-domain-age.py example.com -o results.csv

# 4. Check another domain and save results:
# python analyze-domain-age.py google.com -o google_results.csv