Great idea — this is a **very natural fit for Streamlit + JSON**, and it scales well as your course planning grows.

Below I’ll give you:

1. **Conceptual model (how things relate)**
2. **Recommended project directory structure**
3. **JSON schema (clean, future-proof)**
4. **Concrete JSON example for your provided course**
5. **How this maps cleanly to a Streamlit app**

No images needed here — structure and clarity matter more.

---

## 1️⃣ Conceptual Model (Mental Map)

Your planning hierarchy is:

```
You
└── Minor Program
    ├── Metadata (name, ECTS range, link)
    └── Courses
        ├── Course metadata
        ├── Learning outcomes
        ├── Content
        ├── Teaching & study methods
        ├── Assessment
        └── Admin info (language, level, person in charge)
```

Key design choice:

* **Minor programs are containers**
* **Courses are atomic units**
* Each course lives in its **own JSON file** → easier to maintain & reuse

---

## 2️⃣ Recommended Project Directory Structure

This structure works well for:

* Streamlit
* Version control
* Incremental expansion (notes, progress, ratings later)

```
course_planner/
│
├── app.py                         # Main Streamlit entry
│
├── data/
│   ├── minors/
│   │   ├── minor_cs_for_ds.json   # Minor-level metadata
│   │
│   └── courses/
│       ├── 811104P.json           # One file per course
│       ├── 811105P.json
│       └── ...
│
├── pages/
│   ├── 1_minor_overview.py        # Select minor, see structure
│   ├── 2_course_browser.py        # Browse courses
│   └── 3_course_detail.py         # Deep dive per course
│
├── modules/
│   ├── loaders.py                 # JSON loading utilities
│   ├── models.py                  # (Optional) schema helpers
│   └── ui_components.py           # Reusable Streamlit UI blocks
│
├── README.md
└── requirements.txt
```

Why this works well:

* `data/` is **pure content**
* `pages/` is **pure UI**
* `modules/` keeps logic clean

---

## 3️⃣ JSON Schema Design

### A. Minor Program JSON (container)

**File:** `data/minors/minor_cs_for_ds.json`

```json

```

Design notes:

* `courses` references course IDs → **no duplication**
* Easy to add notes like *“good fit with ML track”*

---

### B. Course JSON (atomic unit)

**File:** `data/courses/811104P.json`

```json

```

Why this schema is solid:

* Everything is **structured**, not free text blobs
* Lists are searchable & filterable
* Teaching hours are numeric → future workload analysis possible

---

## 4️⃣ How This Maps to Streamlit (High Level)

Later, your Streamlit flow becomes trivial:

* **Select Minor**

  * Load `data/minors/*.json`
* **List Courses**

  * Resolve IDs → load course JSONs
* **Course Detail Page**

  * Render sections using expanders:

    * Learning outcomes
    * Content
    * Assessment
    * Teaching workload

You can later add:

* ✔ Completed checkbox
* ⭐ Difficulty rating
* 🧠 Personal notes
* 📊 ECTS progress bar

All without changing the base schema.

---

## 5️⃣ Why This Design Will Age Well

* Works for **multiple minors**
* Works for **multiple academic years**
* Easy to export → CV, portfolio, study plan
* JSON is human-readable + machine-friendly

---

If you want, next we can:

* Build **`loaders.py`**
* Create the **first Streamlit page**
* Add **ECTS progress visualization**
* Add **personal reflections & completion tracking**

Just tell me the next step.
# course_planning
