from flask import Flask, render_template, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load data
kentucky_df = pd.read_csv('templates/data/Kentucky_cleaned.csv')
northdakota_df = pd.read_csv('templates/data/NorthDakota_cleaned.csv')
alaska_df = pd.read_csv('templates/data/Alaska_cleaned.csv')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api/disciplines')
def get_disciplines():
    try:
        all_data = pd.concat([kentucky_df, northdakota_df, alaska_df])
        disciplines = all_data['Discipline'].dropna().unique().tolist()
        disciplines = sorted(list(set(disciplines)))
        return jsonify({'disciplines': disciplines})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/disciplinary-data')
def get_disciplinary_data():
    state = request.args.get('state', 'All')
    discipline = request.args.get('discipline', 'All')
    
    try:
        if state == 'Kentucky':
            df = kentucky_df
        elif state == 'NorthDakota':
            df = northdakota_df
        elif state == 'Alaska':
            df = alaska_df
        else:
            df = pd.concat([kentucky_df, northdakota_df, alaska_df])
        
        if discipline != 'All':
            df = df[df['Discipline'] == discipline]

        categories = {
            'Students_wo_w_Disabilities': 'W/ & W/out Disabilities',
            'Section504': 'Under Section 504',
            'IDEA': 'Under IDEA',
            'Race_AmericanIndian': 'American Indian',
            'Race_Asian': 'Asian',
            'Race_Hispanic': 'Hispanic',
            'Race_Black': 'Black',
            'Race_White': 'White',
            'Race_NativeHawaiian': 'Native Hawaiian/Pacific Islander',
            'Race_TwoOrMore': 'Two or More Races',
            'ELL': 'English Language Learners'
        }

        male_counts = []
        female_counts = []
        labels = []

        for prefix, label in categories.items():
            male_col = f'{prefix}_Male_Number'
            female_col = f'{prefix}_Female_Number'
            if male_col in df.columns and female_col in df.columns:
                male_counts.append(int(df[male_col].sum()))
                female_counts.append(int(df[female_col].sum()))
                labels.append(label)

        return jsonify({
            'categories': labels,
            'male_counts': male_counts,
            'female_counts': female_counts
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/disability-data')
def get_disability_data():
    try:
        datasets = [
            ('Kentucky', kentucky_df),
            ('North Dakota', northdakota_df),
            ('Alaska', alaska_df)
        ]

        categories = ['Without Disabilities', 'Under Section 504', 'Under IDEA']
        data_by_state = {}

        for state_name, df in datasets:
            without_disabilities = (
                df['Students_wo_w_Disabilities_Female_Number'].sum() +
                df['Students_wo_w_Disabilities_Male_Number'].sum()
            )
            section504 = (
                df['Section504_Female_Number'].sum() +
                df['Section504_Male_Number'].sum()
            )
            idea = (
                df['IDEA_Female_Number'].sum() +
                df['IDEA_Male_Number'].sum()
            )

            data_by_state[state_name] = [int(without_disabilities), int(section504), int(idea)]

        return jsonify({
            'labels': categories,
            'kentucky_counts': data_by_state['Kentucky'],
            'northdakota_counts': data_by_state['North Dakota'],
            'alaska_counts': data_by_state['Alaska']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ell-data')
def get_ell_data():
    try:
        ell_data = {
            'labels': ['Kentucky', 'North Dakota', 'Alaska'],
            'data': []
        }

        for state_name, df in [('Kentucky', kentucky_df), ('North Dakota', northdakota_df), ('Alaska', alaska_df)]:
            total = int(df['ELL_Male_Number'].sum() + df['ELL_Female_Number'].sum())
            ell_data['data'].append(total)

        return jsonify(ell_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
   
if __name__ == "__main__":
    app.run(debug=True)
