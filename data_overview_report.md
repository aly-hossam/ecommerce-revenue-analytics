# Data Inspection & Overview Report

**Root Directory:** `/root/Desktop/Project_4`

---

## Dataset: `extracted_files/Maven+Fuzzy+Factory/maven_fuzzy_factory_data_dictionary.csv`

### 1. General Overview
- **Total Rows:** `36`
- **Total Columns:** `3`
- **Duplicate Rows:** `0` (0.00%)

### 2. Columns Profiling
| Column Name | Data Type | Non-Null | Missing Count | Missing % | Unique Values | Sample Value |
| --- | --- | --- | --- | --- | --- | --- |
| `Table` | `object` | 36 | 0 | 0.00% | 6 | orders |
| `Field` | `object` | 36 | 0 | 0.00% | 22 | order_id |
| `Description` | `object` | 36 | 0 | 0.00% | 34 | Unique identifier for each ... |


### 4. Data Preview (First 5 Rows)
| Table | Field | Description |
| --- | --- | --- |
| orders | order_id | Unique identifier for each order (PK) |
| orders | created_at | Timestamp when the order was placed |
| orders | website_session_id | Unique identifier for the website session (FK) |
| orders | user_id | Unique identifier for the user (FK) |
| orders | primary_product_id | Unique identifier for the primary product in the order if part of a bundle (FK) |

---

## Dataset: `extracted_files/Maven+Fuzzy+Factory/orders.csv`

### 1. General Overview
- **Total Rows:** `32,313`
- **Total Columns:** `8`
- **Duplicate Rows:** `0` (0.00%)

### 2. Columns Profiling
| Column Name | Data Type | Non-Null | Missing Count | Missing % | Unique Values | Sample Value |
| --- | --- | --- | --- | --- | --- | --- |
| `order_id` | `int64` | 32,313 | 0 | 0.00% | 32,313 | 1 |
| `created_at` | `object` | 32,313 | 0 | 0.00% | 32,299 | 2012-03-19 10:42:46 |
| `website_session_id` | `int64` | 32,313 | 0 | 0.00% | 32,313 | 20 |
| `user_id` | `int64` | 32,313 | 0 | 0.00% | 31,696 | 20 |
| `primary_product_id` | `int64` | 32,313 | 0 | 0.00% | 4 | 1 |
| `items_purchased` | `int64` | 32,313 | 0 | 0.00% | 2 | 1 |
| `price_usd` | `float64` | 32,313 | 0 | 0.00% | 10 | 49.99 |
| `cogs_usd` | `float64` | 32,313 | 0 | 0.00% | 10 | 19.49 |


### 3. Numerical Summary
| Column | min | 25% | 50% | 75% | max | mean | std |
| --- | --- | --- | --- | --- | --- | --- | --- |
| order_id | 1.0 | 8079.0 | 16157.0 | 24235.0 | 32313.0 | 16157.0 | 9328.103960612789 |
| website_session_id | 20.0 | 144828.0 | 263554.0 | 374799.0 | 472818.0 | 258292.2887073314 | 132427.6498421861 |
| user_id | 13.0 | 124135.0 | 221461.0 | 310542.0 | 394273.0 | 215691.62262866338 | 108402.20318850478 |
| primary_product_id | 1.0 | 1.0 | 1.0 | 2.0 | 4.0 | 1.3924736174295176 | 0.732276970326095 |
| items_purchased | 1.0 | 1.0 | 1.0 | 1.0 | 2.0 | 1.2386655525639836 | 0.42627447731996115 |
| price_usd | 29.99 | 49.99 | 49.99 | 59.99 | 109.98 | 59.99163649305233 | 17.808771047298354 |
| cogs_usd | 9.49 | 19.49 | 19.49 | 22.49 | 41.98 | 22.35540649274286 | 6.2386205589263355 |


### 4. Data Preview (First 5 Rows)
| order_id | created_at | website_session_id | user_id | primary_product_id | items_purchased | price_usd | cogs_usd |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2012-03-19 10:42:46 | 20 | 20 | 1 | 1 | 49.99 | 19.49 |
| 2 | 2012-03-19 19:27:37 | 104 | 104 | 1 | 1 | 49.99 | 19.49 |
| 3 | 2012-03-20 06:44:45 | 147 | 147 | 1 | 1 | 49.99 | 19.49 |
| 4 | 2012-03-20 09:41:45 | 160 | 160 | 1 | 1 | 49.99 | 19.49 |
| 5 | 2012-03-20 11:28:15 | 177 | 177 | 1 | 1 | 49.99 | 19.49 |

---

## Dataset: `extracted_files/Maven+Fuzzy+Factory/order_items.csv`

### 1. General Overview
- **Total Rows:** `40,025`
- **Total Columns:** `7`
- **Duplicate Rows:** `0` (0.00%)

### 2. Columns Profiling
| Column Name | Data Type | Non-Null | Missing Count | Missing % | Unique Values | Sample Value |
| --- | --- | --- | --- | --- | --- | --- |
| `order_item_id` | `int64` | 40,025 | 0 | 0.00% | 40,025 | 1 |
| `created_at` | `object` | 40,025 | 0 | 0.00% | 32,299 | 2012-03-19 10:42:46 |
| `order_id` | `int64` | 40,025 | 0 | 0.00% | 32,313 | 1 |
| `product_id` | `int64` | 40,025 | 0 | 0.00% | 4 | 1 |
| `is_primary_item` | `int64` | 40,025 | 0 | 0.00% | 2 | 1 |
| `price_usd` | `float64` | 40,025 | 0 | 0.00% | 4 | 49.99 |
| `cogs_usd` | `float64` | 40,025 | 0 | 0.00% | 4 | 19.49 |


### 3. Numerical Summary
| Column | min | 25% | 50% | 75% | max | mean | std |
| --- | --- | --- | --- | --- | --- | --- | --- |
| order_item_id | 1.0 | 10007.0 | 20013.0 | 30019.0 | 40025.0 | 20013.0 | 11554.366598823148 |
| order_id | 1.0 | 9871.0 | 17490.0 | 24818.0 | 32313.0 | 17121.957501561523 | 9053.765867416096 |
| product_id | 1.0 | 1.0 | 1.0 | 2.0 | 4.0 | 1.7700187382885697 | 1.0855613736917362 |
| is_primary_item | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.8073204247345409 | 0.3944084723519855 |
| price_usd | 29.99 | 49.99 | 49.99 | 49.99 | 59.99 | 48.432473454091195 | 8.012370188188662 |
| cogs_usd | 9.49 | 19.49 | 19.49 | 19.49 | 22.49 | 18.047976264834478 | 3.856820952703982 |


### 4. Data Preview (First 5 Rows)
| order_item_id | created_at | order_id | product_id | is_primary_item | price_usd | cogs_usd |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2012-03-19 10:42:46 | 1 | 1 | 1 | 49.99 | 19.49 |
| 2 | 2012-03-19 19:27:37 | 2 | 1 | 1 | 49.99 | 19.49 |
| 3 | 2012-03-20 06:44:45 | 3 | 1 | 1 | 49.99 | 19.49 |
| 4 | 2012-03-20 09:41:45 | 4 | 1 | 1 | 49.99 | 19.49 |
| 5 | 2012-03-20 11:28:15 | 5 | 1 | 1 | 49.99 | 19.49 |

---

## Dataset: `extracted_files/Maven+Fuzzy+Factory/order_item_refunds.csv`

### 1. General Overview
- **Total Rows:** `1,731`
- **Total Columns:** `5`
- **Duplicate Rows:** `0` (0.00%)

### 2. Columns Profiling
| Column Name | Data Type | Non-Null | Missing Count | Missing % | Unique Values | Sample Value |
| --- | --- | --- | --- | --- | --- | --- |
| `order_item_refund_id` | `int64` | 1,731 | 0 | 0.00% | 1,731 | 1 |
| `created_at` | `object` | 1,731 | 0 | 0.00% | 1,731 | 2012-04-06 11:32:43 |
| `order_item_id` | `int64` | 1,731 | 0 | 0.00% | 1,731 | 57 |
| `order_id` | `int64` | 1,731 | 0 | 0.00% | 1,723 | 57 |
| `refund_amount_usd` | `float64` | 1,731 | 0 | 0.00% | 4 | 49.99 |


### 3. Numerical Summary
| Column | min | 25% | 50% | 75% | max | mean | std |
| --- | --- | --- | --- | --- | --- | --- | --- |
| order_item_refund_id | 1.0 | 433.5 | 866.0 | 1298.5 | 1731.0 | 866.0 | 499.8409747109574 |
| order_item_id | 57.0 | 7417.0 | 19858.0 | 26900.0 | 39950.0 | 18472.214904679375 | 11438.074606458997 |
| order_id | 57.0 | 7412.0 | 17375.0 | 22539.5 | 32255.0 | 15868.242056614674 | 9096.061945063195 |
| refund_amount_usd | 29.99 | 49.99 | 49.99 | 49.99 | 59.99 | 49.3002253032929 | 4.9560151466858855 |


### 4. Data Preview (First 5 Rows)
| order_item_refund_id | created_at | order_item_id | order_id | refund_amount_usd |
| --- | --- | --- | --- | --- |
| 1 | 2012-04-06 11:32:43 | 57 | 57 | 49.99 |
| 2 | 2012-04-13 01:09:43 | 74 | 74 | 49.99 |
| 3 | 2012-04-15 07:03:48 | 71 | 71 | 49.99 |
| 4 | 2012-04-17 20:00:37 | 118 | 118 | 49.99 |
| 5 | 2012-04-22 20:53:49 | 116 | 116 | 49.99 |

---

## Dataset: `extracted_files/Maven+Fuzzy+Factory/products.csv`

### 1. General Overview
- **Total Rows:** `4`
- **Total Columns:** `3`
- **Duplicate Rows:** `0` (0.00%)

### 2. Columns Profiling
| Column Name | Data Type | Non-Null | Missing Count | Missing % | Unique Values | Sample Value |
| --- | --- | --- | --- | --- | --- | --- |
| `product_id` | `int64` | 4 | 0 | 0.00% | 4 | 1 |
| `created_at` | `object` | 4 | 0 | 0.00% | 4 | 2012-03-19 08:00:00 |
| `product_name` | `object` | 4 | 0 | 0.00% | 4 | The Original Mr. Fuzzy |


### 3. Numerical Summary
| Column | min | 25% | 50% | 75% | max | mean | std |
| --- | --- | --- | --- | --- | --- | --- | --- |
| product_id | 1.0 | 1.75 | 2.5 | 3.25 | 4.0 | 2.5 | 1.2909944487358056 |


### 4. Data Preview (First 5 Rows)
| product_id | created_at | product_name |
| --- | --- | --- |
| 1 | 2012-03-19 08:00:00 | The Original Mr. Fuzzy |
| 2 | 2013-01-06 13:00:00 | The Forever Love Bear |
| 3 | 2013-12-12 09:00:00 | The Birthday Sugar Panda |
| 4 | 2014-02-05 10:00:00 | The Hudson River Mini bear |

---

## Dataset: `extracted_files/Maven+Fuzzy+Factory/website_pageviews.csv`

### 1. General Overview
- **Total Rows:** `1,188,124`
- **Total Columns:** `4`
- **Duplicate Rows:** `0` (0.00%)

### 2. Columns Profiling
| Column Name | Data Type | Non-Null | Missing Count | Missing % | Unique Values | Sample Value |
| --- | --- | --- | --- | --- | --- | --- |
| `website_pageview_id` | `int64` | 1,188,124 | 0 | 0.00% | 1,188,124 | 1 |
| `created_at` | `object` | 1,188,124 | 0 | 0.00% | 1,171,962 | 2012-03-19 08:04:16 |
| `website_session_id` | `int64` | 1,188,124 | 0 | 0.00% | 472,871 | 1 |
| `pageview_url` | `object` | 1,188,124 | 0 | 0.00% | 16 | /home |


### 3. Numerical Summary
| Column | min | 25% | 50% | 75% | max | mean | std |
| --- | --- | --- | --- | --- | --- | --- | --- |
| website_pageview_id | 1.0 | 297031.75 | 594062.5 | 891093.25 | 1188124.0 | 594062.5 | 342981.99995389074 |
| website_session_id | 1.0 | 127786.0 | 247808.0 | 362739.0 | 472871.0 | 244458.51508428412 | 135619.8615243083 |


### 4. Data Preview (First 5 Rows)
| website_pageview_id | created_at | website_session_id | pageview_url |
| --- | --- | --- | --- |
| 1 | 2012-03-19 08:04:16 | 1 | /home |
| 2 | 2012-03-19 08:16:49 | 2 | /home |
| 3 | 2012-03-19 08:26:55 | 3 | /home |
| 4 | 2012-03-19 08:37:33 | 4 | /home |
| 5 | 2012-03-19 09:00:55 | 5 | /home |

---

## Dataset: `extracted_files/Maven+Fuzzy+Factory/website_sessions.csv`

### 1. General Overview
- **Total Rows:** `472,871`
- **Total Columns:** `9`
- **Duplicate Rows:** `0` (0.00%)

### 2. Columns Profiling
| Column Name | Data Type | Non-Null | Missing Count | Missing % | Unique Values | Sample Value |
| --- | --- | --- | --- | --- | --- | --- |
| `website_session_id` | `int64` | 472,871 | 0 | 0.00% | 472,871 | 1 |
| `created_at` | `object` | 472,871 | 0 | 0.00% | 470,444 | 2012-03-19 08:04:16 |
| `user_id` | `int64` | 472,871 | 0 | 0.00% | 394,318 | 1 |
| `is_repeat_session` | `int64` | 472,871 | 0 | 0.00% | 2 | 0 |
| `utm_source` | `object` | 389,543 | 83,328 | 17.62% | 3 | gsearch |
| `utm_campaign` | `object` | 389,543 | 83,328 | 17.62% | 4 | nonbrand |
| `utm_content` | `object` | 389,543 | 83,328 | 17.62% | 6 | g_ad_1 |
| `device_type` | `object` | 472,871 | 0 | 0.00% | 2 | mobile |
| `http_referer` | `object` | 432,954 | 39,917 | 8.44% | 3 | https://www.gsearch.com |


### 3. Numerical Summary
| Column | min | 25% | 50% | 75% | max | mean | std |
| --- | --- | --- | --- | --- | --- | --- | --- |
| website_session_id | 1.0 | 118218.5 | 236436.0 | 354653.5 | 472871.0 | 236436.0 | 136506.24390847475 |
| user_id | 1.0 | 101966.5 | 199483.0 | 294433.0 | 394318.0 | 198037.97016311003 | 111992.9977984035 |
| is_repeat_session | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.166119301035589 | 0.3721880865917451 |


### 4. Data Preview (First 5 Rows)
| website_session_id | created_at | user_id | is_repeat_session | utm_source | utm_campaign | utm_content | device_type | http_referer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2012-03-19 08:04:16 | 1 | 0 | gsearch | nonbrand | g_ad_1 | mobile | https://www.gsearch.com |
| 2 | 2012-03-19 08:16:49 | 2 | 0 | gsearch | nonbrand | g_ad_1 | desktop | https://www.gsearch.com |
| 3 | 2012-03-19 08:26:55 | 3 | 0 | gsearch | nonbrand | g_ad_1 | desktop | https://www.gsearch.com |
| 4 | 2012-03-19 08:37:33 | 4 | 0 | gsearch | nonbrand | g_ad_1 | desktop | https://www.gsearch.com |
| 5 | 2012-03-19 09:00:55 | 5 | 0 | gsearch | nonbrand | g_ad_1 | mobile | https://www.gsearch.com |

---
