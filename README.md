# 🍽️ Zomato Restaurant Analysis

An end-to-end data analytics project on Bangalore restaurant data from Zomato, covering
**data exploration and cleaning in Python**, **storage in MySQL**, and an **interactive dashboard in Tableau**.

### 🔗 [View the Live Tableau Dashboard](https://public.tableau.com/app/profile/khushi.bucha/viz/ZomatoRestaurantAnalyticsDashboard_17934680341110/Dashboard1)

---

## 📌 Project Objective

Analyse restaurant listings to understand:

- How restaurants are distributed across Bangalore areas
- Which restaurant types get the highest ratings
- Whether offering **online ordering** relates to better ratings
- Overall pricing (average cost for two) and rating trends

---

## 🛠️ Tools & Technologies

| Stage            | Tool                          |
|------------------|-------------------------------|
| Data Cleaning    | Python (pandas, numpy)        |
| Database         | MySQL 8+ / MySQL Workbench    |
| Visualisation    | Tableau Public                |

---

## 📁 Project Structure

```
Zomato-Restaurant-Analysis/
├── Data/
│   ├── Raw/
│   │   └── zomato.csv               # Original dataset (~574 MB, not cleaned)
│   └── Processed/
│       └── zomato_cleaned.csv       # Cleaned, SQL-ready dataset (~11 MB)
├── Scripts/
│   ├── data_exploration.py          # Initial data exploration (EDA)
│   └── data_cleaning.py             # Cleaning pipeline -> zomato_cleaned.csv
├── Sql/
│   └── zomato_analysis.sql          # Database, table creation & data import
├── Dashboard/                       # Tableau dashboard files
├── reports/                         # Reports / findings
├── requirements.txt
└── README.md
```

---

## 📊 Dataset

- **Source:** Zomato Bangalore Restaurants dataset (`zomato.csv`)
- **Raw size:** 51,717 rows × 17 columns
- **Cleaned size:** 51,632 rows × 14 columns

### Cleaned Columns

| Column         | Description                                   |
|----------------|-----------------------------------------------|
| `name`         | Restaurant name                               |
| `address`      | Full address                                  |
| `online_order` | Accepts online orders (Yes / No)              |
| `book_table`   | Accepts table booking (Yes / No)              |
| `rate`         | Rating out of 5                               |
| `votes`        | Number of votes                               |
| `phone`        | Contact number(s)                             |
| `location`     | Neighbourhood of the restaurant               |
| `rest_type`    | Restaurant type (Cafe, Casual Dining, ...)    |
| `dish_liked`   | Popular dishes                                |
| `cuisines`     | Cuisines served                               |
| `approx_cost`  | Approximate cost for two people (₹)           |
| `listed_type`  | Listing category (Buffet, Delivery, Dine-out, ...) |
| `listed_city`  | Area the restaurant is listed under           |

---

## 🧹 Data Cleaning Steps (`Scripts/data_cleaning.py`)

1. Stripped extra spaces from column names and text values
2. Extracted numeric ratings from text such as `"4.1/5"`; values like `"NEW"` or `"-"` → NULL
3. Removed commas from cost (`"1,200"` → `1200`) and converted it to a number
4. Converted empty strings in text columns to NULL
5. Dropped very large text columns (`reviews_list`, `menu_item`, `url`) to make the file SQL-friendly
6. Replaced line breaks inside `phone` with `", "` so each record stays on one line
7. Renamed columns with brackets → `approx_cost`, `listed_type`, `listed_city`
8. Stored `votes` and `approx_cost` as whole numbers
9. Removed **85 duplicate rows**
10. Validated the output: ratings fall between 0 and 5, there are no duplicates, and the saved file shape matches

---

## 🗄️ SQL Setup (`Sql/zomato_analysis.sql`)

The script:

1. Creates the database `zomato_db` (utf8mb4)
2. Creates the `restaurants` table
3. Loads `zomato_cleaned.csv` using `LOAD DATA LOCAL INFILE` (empty values → NULL)
4. Runs validation queries (expected **51,632** rows)

**Before running it in MySQL Workbench:**

```sql
SET GLOBAL local_infile = 1;
```

Then go to **Edit Connection → Advanced → Others**, add `OPT_LOCAL_INFILE=1`, and reconnect.

---

## 📈 Tableau Dashboard

**[Zomato Restaurant Analytics Dashboard](https://public.tableau.com/app/profile/khushi.bucha/viz/ZomatoRestaurantAnalyticsDashboard_17934680341110/Dashboard1)**

### KPIs

| Metric             | Value      |
|--------------------|------------|
| Total Restaurants (listings) | **51,632** |
| Average Rating     | **3.70**   |
| Average Cost for Two | **₹555** |
| Total Locations (listed areas) | **30** |

### Visuals

- **Average Rating by Restaurant Type:** the top 10 restaurant types by average rating
- **Restaurant Count by Location:** the top 10 areas by number of listings
- **Online Order vs Rating:** average rating with and without online ordering
- **Online Ordering Analysis:** number of restaurants that do and do not offer online ordering

---

## 💡 Key Insights

1. **Pubs, bars and microbreweries are the highest rated.** *Pub, Cafe* (4.66), *Bar, Pub* (4.60) and *Microbrewery* (4.48) lead the ratings.
2. **BTM has the most listings (3,268).** The Koramangala blocks (5th, 6th, 7th, 4th) follow it, so these areas are the most competitive markets.
3. **Most restaurants offer online ordering.** About **59%** of listings (30,379 of 51,632) accept online orders.
4. **Online ordering is linked to slightly better ratings.** Restaurants with online ordering average **3.72**, compared with **3.66** for those without.
5. **Ratings are moderate overall.** The average rating is 3.70, and the typical cost for two is about ₹555.

> **Note:** Restaurants appear more than once in the dataset because the same outlet is listed under several
> categories and areas. The 51,632 figure counts **listings**; the dataset has about **12,494 unique restaurants**.

---

## ▶️ How to Run

```bash
# 1. Create & activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Explore the raw data
python Scripts/data_exploration.py

# 4. Clean the data -> Data/Processed/zomato_cleaned.csv
python Scripts/data_cleaning.py
```

5. Open `Sql/zomato_analysis.sql` in MySQL Workbench and run it to load the data.
6. Open the Tableau dashboard from the link above.

---

## 👤 Author

**Khushi Bucha**
[Tableau Public Profile](https://public.tableau.com/app/profile/khushi.bucha)
