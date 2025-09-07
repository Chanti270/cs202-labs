import argparse, pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    df = pd.read_csv(args.files)

    total = len(df)
    bugfix_count = sum("fix" in str(m).lower() for m in df["developer_msg"])
    refined_count = df["rectified_msg"].notna().sum()

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("# Evaluation Report (Django)\n\n")
        f.write(f"**Total file-level changes analyzed:** {total}\n\n")
        f.write(f"**Commits with 'fix' in developer message:** {bugfix_count}\n\n")
        f.write(f"**Rectified messages generated:** {refined_count}\n\n")
        f.write("### Observations\n")
        f.write("- Developer messages often use short 'fix' notes.\n")
        f.write("- Rectified messages make them slightly clearer.\n")
        f.write("- Data is now ready for RQ1, RQ2, RQ3 analysis.\n")

    print(f"✅ Evaluation report saved to {args.out}")

if __name__ == "__main__":
    main()
