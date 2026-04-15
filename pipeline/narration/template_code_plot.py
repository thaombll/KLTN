import pandas as pd
import matplotlib.pyplot as plt
import os
import re


def load_table(table_name):
    path = f"data\\Test\\Tableau\\tab_003\\{table_name}.csv"
    return pd.read_csv(path)

def clean_numeric(series):
    return (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
    )

def safe_filename(text):
    return re.sub(r"[^\w\-]", "_", text)

def save_plot(section):
    os.makedirs("result", exist_ok=True)
    filename = safe_filename(section) + ".png"
    path = f"result/{filename}"
    plt.savefig(path)
    plt.close()
    return path

# ===== BAR =====
def plot_bar(table_name, section, x, y, title, xlabel="", ylabel="", top_n=20):
    df = load_table(table_name)

    if x not in df.columns or y not in df.columns:
        raise ValueError(f"Column không tồn tại: {x}, {y}")

    df[y] = clean_numeric(df[y])

    try:
        df[y] = df[y].astype(float)
    except:
        raise ValueError(f"{y} không phải numeric")

    df = df.sort_values(by=y, ascending=False).head(top_n)

    x_data = df[x]
    y_data = df[y]

    plt.figure()
    colors = ["red" if v < 0 else "green" for v in y_data]
    plt.bar(x_data, y_data, color=colors)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()

    return save_plot(section)


# ===== TREND =====
def plot_trend(table_name, section, title, xlabel="", ylabel=""):
    df = load_table(table_name)

    df = df.dropna(how="all")

    years = df.columns[1:]

    y_data = []

    for col in years:
        col_data = clean_numeric(df[col])
        col_data = pd.to_numeric(col_data, errors="coerce")
        y_data.append(col_data.mean())

    x_data = years

    plt.figure()
    plt.plot(x_data, y_data, marker='o')

    plt.title(title)
    plt.xlabel(xlabel or "Time")
    plt.ylabel(ylabel or "Value")
    plt.xticks(rotation=45)
    plt.tight_layout()

    return save_plot(section)


# ===== SCATTER =====
def plot_scatter(table_name, section, x, y, title, xlabel="", ylabel=""):
    df = load_table(table_name)

    if x not in df.columns or y not in df.columns:
        raise ValueError(f"Column không tồn tại: {x}, {y}")

    df[x] = clean_numeric(df[x])
    df[y] = clean_numeric(df[y])

    df[x] = pd.to_numeric(df[x], errors="coerce")
    df[y] = pd.to_numeric(df[y], errors="coerce")

    df = df.dropna(subset=[x, y])

    plt.figure()
    plt.scatter(df[x], df[y])

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()

    return save_plot(section)


# ===== BUBBLE =====
def plot_bubble(table_name, section, x, y, size, title, xlabel="", ylabel=""):
    df = load_table(table_name)

    for col in [x, y, size]:
        if col not in df.columns:
            raise ValueError(f"Column không tồn tại: {col}")

    df[x] = pd.to_numeric(clean_numeric(df[x]), errors="coerce")
    df[y] = pd.to_numeric(clean_numeric(df[y]), errors="coerce")
    df[size] = pd.to_numeric(clean_numeric(df[size]), errors="coerce")

    df = df.dropna(subset=[x, y, size])

    plt.figure()
    plt.scatter(df[x], df[y], s=df[size])

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()

    return save_plot(section)

def plot_bar_line(table_name, section, x, bar_values, line_values, title,
                  xlabel="", ylabel_bar="", ylabel_line=""):

    df = load_table(table_name)

    for col in [x, bar_values, line_values]:
        if col not in df.columns:
            raise ValueError(f"Column không tồn tại: {col}")

    df[bar_values] = pd.to_numeric(clean_numeric(df[bar_values]), errors="coerce")
    df[line_values] = pd.to_numeric(clean_numeric(df[line_values]), errors="coerce")

    df = df.dropna(subset=[bar_values, line_values])

    x_data = df[x]

    fig, ax1 = plt.subplots()

    ax1.bar(x_data, df[bar_values])
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel_bar)

    ax2 = ax1.twinx()
    ax2.plot(x_data, df[line_values], marker='o')
    ax2.set_ylabel(ylabel_line)

    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()

    return save_plot(section)

def plot(df):
    save_paths = []

    for i in range(len(df)):
        row = df.iloc[i]

        try:
            if row["plot_type"] == "bar":
                path = plot_bar(
                    row["table_name"],
                    row["section"],
                    row["x"],
                    row["y"],
                    row["title"],
                    row["xlabel"],
                    row["ylabel"]
                )

            elif row["plot_type"] == "scatter":
                path = plot_scatter(
                    row["table_name"],
                    row["section"],
                    row["x"],
                    row["y"],
                    row["title"],
                    row["xlabel"],
                    row["ylabel"]
                )

            elif row["plot_type"] == "trend":
                path = plot_trend(
                    row["table_name"],
                    row["section"],
                    row["title"],
                    row["xlabel"],
                    row["ylabel"]
                )

            elif row["plot_type"] == "bubble":
                path = plot_bubble(
                    row["table_name"],
                    row["section"],
                    row["x"],
                    row["y"],
                    row["size"],
                    row["title"],
                    row["xlabel"],
                    row["ylabel"]
                )

            elif row["plot_type"] == "bar_line":
                path = plot_bar_line(
                    row["table_name"],
                    row["section"],
                    row["x"],
                    row["bar_values"],
                    row["line_values"],
                    row["title"],
                    row["xlabel"],
                    row["ylabel_bar"],
                    row["ylabel_line"]
                )

            else:
                path = None

        except Exception as e:
            print(f"Lỗi tại section '{row['section']}': {e}")
            path = None

        save_paths.append(path)

    df["plot_path"] = save_paths
    return df