from flask import Flask, render_template
import pandas as pd
import os

class DataLoader:
    """Handles data loading and processing for various datasets."""

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FOLDER = os.path.join(BASE_DIR, "templates", "data")

    @classmethod
    def load_csv(cls, filename, required_columns):
        """Generic method to load CSV data and validate required columns."""
        file_path = os.path.join(cls.DATA_FOLDER, filename)
        if not os.path.exists(file_path):
            print(f"\u274C ERROR: Dataset '{filename}' not found.")
            return pd.DataFrame()
        
        df = pd.read_csv(file_path)
        for col in required_columns:
            if col not in df.columns:
                print(f"\u274C ERROR: Missing column '{col}' in dataset! Available: {df.columns}")
                return pd.DataFrame()
        return df

    @classmethod
    def load_discipline_data(cls):
        """Load and clean discipline data, aggregating cases by race/ethnicity."""
        file_path = os.path.join(cls.DATA_FOLDER, "discipline_data.csv")
        
        if not os.path.exists(file_path):
            return {}
        
        df = pd.read_csv(file_path).fillna(0)
        df.columns = df.columns.str.strip()

        race_columns = [
            "American Indian or Alaska Native Number",
            "Asian Number",
            "Hispanic or Latino of any race Number",
            "Black or African American Number",
            "White Number",
            "Native Hawaiian or Other Pacific Islander Number",
            "Two or more races Number"
        ]

        missing_columns = [col for col in race_columns if col not in df.columns]
        if missing_columns:
            print(f"\u274C ERROR: Missing columns in dataset: {missing_columns}")
            return {}

        for col in race_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        discipline_counts = {race: int(df[race].sum()) for race in race_columns}

        return discipline_counts
    
    @classmethod
    def load_schools_data(cls):
        """Load and process the number of schools per state."""
        file_path = os.path.join(cls.DATA_FOLDER, "public_school_datapysical.csv")

        if not os.path.exists(file_path):
            print(f"\u274C ERROR: Dataset 'public_school_datapysical.csv' not found!")
            return {}
        
        df = pd.read_csv(file_path).fillna(0)
        df.columns = df.columns.str.strip()

        required_columns = ["State", "Number of Schools"]
        for col in required_columns:
            if col not in df.columns:
                print(f"\u274C ERROR: Missing column '{col}' in dataset!")
                return {}
        
        df["Number of Schools"] = pd.to_numeric(df["Number of Schools"], errors='coerce').fillna(0).astype(int)
        schools_data = df.set_index("State")["Number of Schools"].to_dict()
        return schools_data
    
    @classmethod
    def load_disability_data(cls):
        """Load and process data on students with disabilities."""
        file_path = os.path.join(cls.DATA_FOLDER, "public_school_datapysical.csv")
        
        if not os.path.exists(file_path):
            print("\u274C ERROR: Disability data file not found!")
            return {}
        
        df = pd.read_csv(file_path).fillna(0)
        df.columns = df.columns.str.strip()
        
        required_columns = [
            "Students With Disabilities Served Under IDEA Number",
            "Students With Disabilities Served Only Under Section 504 Number",
            "Total Students"
        ]
        
        if not all(col in df.columns for col in required_columns):
            print("\u274C ERROR: Missing required disability columns!")
            return {}
        
        df[required_columns] = df[required_columns].apply(pd.to_numeric, errors='coerce').fillna(0)
        total_students = df["Total Students"].sum()
        idea_students = df["Students With Disabilities Served Under IDEA Number"].sum()
        section_504_students = df["Students With Disabilities Served Only Under Section 504 Number"].sum()
        
        disability_data = {
            "IDEA": int(idea_students),
            "Section 504": int(section_504_students),
            "No Disabilities": int(total_students - idea_students - section_504_students)
        }
        
        return disability_data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route('/stats')
def stats():
    discipline_data = DataLoader.load_discipline_data()
    schools_data = DataLoader.load_schools_data()
    disability_data = DataLoader.load_disability_data()
    
    return render_template("stats.html", 
                           discipline_data=discipline_data, 
                           schools_data=schools_data,
                           disability_data=disability_data)

if __name__ == "__main__":
    app.run(debug=True)