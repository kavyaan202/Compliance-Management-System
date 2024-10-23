
from flask import Flask, render_template, request, redirect, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS

app = Flask(__name__)

# Configure the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/StatutoryDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Compliance model
class Compliance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Compliance_Details = db.Column(db.String(500), nullable=False)
    Name_of_Statutory = db.Column(db.String(100), nullable=False)
    Frequency = db.Column(db.String(50), nullable=False)
    Document_Reference_Number=db.Column(db.String(50), nullable=False)
    Valid_From = db.Column(db.String(20), nullable=False)
    Valid_Upto = db.Column(db.String(20), nullable=False)
    Remarks = db.Column(db.String(500))

class Frequency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    frequency_name = db.Column(db.String(50), nullable=False, unique=True)

categories = {
    'Electrical System': ['Electrical System', 'Transformer', 'Diesel Generator', 'Panels'],
    'Mechanical System': ['Booster pumps', 'Plumbing system'],
    'Water and Waste System': ['Storm water system', 'Sewage treatment plant', 'Water Treatment plant'],
    'Fire Protection System':['Fire Protect System', 'Chute system'],
    'Building Services and Amenities': [ 'Swimming pool'],
    'Security System': ['CCTV', 'Intercom systems']
    }

# Define your options for each subcategory
options = {
        'Electrical System': ['Wiring', 'Circuit Breakers', 'Outlets'],
        'Transformer': ['Step-up', 'Step-down'],
        'Diesel Generator': ['Backup', 'Prime Power'],
        'Panels': ['Control Panel', 'Distribution Panel'],
        'Booster pumps': ['Single-Stage', 'Multistage'],
        'Plumbing system': ['Pipes', 'Fittings'],
        'Storm water system': ['Drains', 'Sump Pumps'],
        'Sewage treatment plant': ['Aeration', 'Clarifiers'],
        'Water Treatment plant': ['Filtration', 'Chlorination'],
        'Fire Protect System': ['Sprinklers', 'Fire Alarms'],
        'Chute system': ['Garbage Chute', 'Laundry Chute'],
        'Swimming pool': ['Chemical Control', 'Filtration System'],
        'CCTV': ['Surveillance Cameras', 'DVR/NVR'],
        'Intercom systems': ['Audio Intercom', 'Video Intercom']
    }

def populate_frequency():
    frequencies = ['One Time', 'Daily', 'Weekly', 'Monthly', 'Quarterly', 'Yearly']
    for freq in frequencies:
        if not Frequency.query.filter_by(frequency_name=freq).first():
            db.session.add(Frequency(frequency_name=freq))
    db.session.commit()

# Run this function in your shell to populate the table



# Function to get unique statutory names for filtering
def get_unique_statutory_names():
    return db.session.query(Compliance.Name_of_Statutory).distinct().order_by(Compliance.Name_of_Statutory).all()

# Function to paginate the compliance list
def paginate_compliances(query, page, per_page=5):
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    return paginated.items, paginated.total

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    statutory_filter = request.args.get('statutory_filter', '')
    per_page = 5

    query = Compliance.query.order_by(Compliance.id)  # Order by ID

    if search_query:
        search = f"%{search_query.lower()}%"
        query = query.filter(
            db.or_(
                func.lower(Compliance.Compliance_Details).like(search),
                func.lower(Compliance.Name_of_Statutory).like(search),
                func.lower(Compliance.Frequency).like(search),
                func.lower(Compliance.Document_Reference_Number).like(search),
                func.lower(Compliance.Valid_From).like(search),
                func.lower(Compliance.Valid_Upto).like(search),
                func.lower(Compliance.Remarks).like(search)
            )
        )

    if statutory_filter:
        query = query.filter(Compliance.Name_of_Statutory == statutory_filter)

    paginated_compliances, total_entries = paginate_compliances(query, page, per_page)

    unique_statutory_names = get_unique_statutory_names()
    total_pages = (total_entries + per_page - 1) // per_page
    frequencies = Frequency.query.all()
    return render_template('index.html', 
                           compliances=paginated_compliances, 
                           statutory_names=unique_statutory_names,
                           total_entries=total_entries,
                           page=page, 
                           total_pages=total_pages,
                           search_query=search_query, 
                           statutory_filter=statutory_filter,
                           frequencies=frequencies
                           )

# Add the complience
# @app.route('/compliance_form')
# def compliance_form():
#     frequencies = Frequency.query.all()
#     return render_template('index.html', frequencies=frequencies)

@app.route('/add_compliance', methods=['POST'])
def add_compliance():
    new_compliance = Compliance(
        Compliance_Details=request.form['Compliance_Details'],
        Name_of_Statutory=request.form['Name_of_Statutory'],
        Frequency=request.form['Frequency'],
        Document_Reference_Number=request.form['Document_Reference_Number'],
        Valid_From=request.form['Valid_From'],
        Valid_Upto=request.form['Valid_Upto'],
        Remarks=request.form['Remarks']
    )
    
    db.session.add(new_compliance)
    db.session.commit()
    
    return redirect(url_for('index'))
# edit complience

@app.route('/edit_compliance/<int:id>', methods=['POST'])
def edit_compliance(id):
    compliance = Compliance.query.get_or_404(id)
    compliance.Compliance_Details = request.form['Compliance_Details']
    compliance.Name_of_Statutory = request.form['Name_of_Statutory']
    compliance.Frequency = request.form['Frequency']
    compliance.Document_Reference_Number=request.form['Document_Reference_Number']
    compliance.Valid_From = request.form['Valid_From']
    compliance.Valid_Upto = request.form['Valid_Upto']
    compliance.Remarks = request.form['Remarks']
    
    db.session.commit()
    
    return redirect(url_for('index'))
# delete complience

@app.route('/delete_compliance/<int:id>', methods=['POST'])
def delete_compliance(id):
    compliance = Compliance.query.get_or_404(id)
    db.session.delete(compliance)
    db.session.commit()
    
    return redirect(url_for('index'))

# from flask import request, render_template, url_for, redirect

@app.route('/compliance_details', methods=['GET', 'POST'])
def compliance_details():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    # Handle form submission
    if request.method == 'POST':
        statutory_filter = request.form.get('statutoryFilter', '')
        # Redirect to GET request with the filter applied
        return redirect(url_for('compliance_details', page=1, statutory_filter=statutory_filter))

    # Process GET parameters
    statutory_filter = request.args.get('statutory_filter', '')

    query = Compliance.query.order_by(Compliance.id)

    if statutory_filter:
        query = query.filter(Compliance.Name_of_Statutory == statutory_filter)

    paginated_compliances, total_entries = paginate_compliances(query, page, per_page)

    unique_statutory_names = get_unique_statutory_names()
    total_pages = (total_entries + per_page - 1) // per_page

    return render_template('compliance_details.html', 
                           compliances=paginated_compliances, 
                           statutory_names=unique_statutory_names,
                           total_entries=total_entries,
                           page=page, 
                           total_pages=total_pages,
                           statutory_filter=statutory_filter)


   
@app.route('/due')
def indexPage():
    return render_template('due_deligence.html')

@app.route('/get_subcategories', methods=['POST'])
def get_subcategories():
    category = request.json['category']
    subcategories = categories.get(category, [])
    return jsonify(subcategories)

@app.route('/get_options', methods=['POST'])
def get_options():
    subcategory = request.json['subcategory']
    options_list = options.get(subcategory, [])
    return jsonify(options_list)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)