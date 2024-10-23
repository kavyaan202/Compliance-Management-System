from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"

# Database connection parameters
DB_HOST = "localhost"
DB_NAME = "sampledb"
DB_USER = "postgres"
DB_PASS = "12345KA@a"

# Route to display the index page
@app.route('/')
def index():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Fetch all compliances to display in the table
        cur.execute("SELECT * FROM compliances")
        list_compliances = cur.fetchall()

        # Fetch distinct regulatory bodies for the dropdown
        cur.execute("SELECT DISTINCT regulatory_body FROM compliances")
        regulatory_bodies = cur.fetchall()
        
        cur.close()
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('index'))
    finally:
        conn.close()

    return render_template('index.html', list_compliances=list_compliances, regulatory_bodies=regulatory_bodies)

# Route to add compliance information
@app.route('/add_compliance', methods=['POST'])
def add_compliance():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if request.method == 'POST':
            regulatory_body = request.form['regulatory_body']
            compliance_detail = request.form['compliance_detail']
            frequency = request.form['frequency']
            doc_ref_no = request.form['doc_ref_no']
            consent_valid_from = request.form['consent_valid_from']
            valid_upto = request.form['valid_upto']
            remarks = request.form['remarks']

            cur.execute(""" 
                INSERT INTO compliances (regulatory_body, compliance_detail, frequency, doc_ref_no, consent_valid_from, valid_upto, remarks) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (regulatory_body, compliance_detail, frequency, doc_ref_no, consent_valid_from, valid_upto, remarks))
            conn.commit()
            flash('Compliance Added Successfully', 'success')
            return redirect(url_for('index'))

    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('index'))
    finally:
        cur.close()
        conn.close()

# Route to edit compliance information
@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_compliance(id):
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if request.method == 'POST':
            regulatory_body = request.form['regulatory_body']
            compliance_detail = request.form['compliance_detail']
            frequency = request.form['frequency']
            doc_ref_no = request.form['doc_ref_no']
            consent_valid_from = request.form['consent_valid_from']
            valid_upto = request.form['valid_upto']
            remarks = request.form['remarks']
            
            # Update the compliance record
            cur.execute(""" 
                UPDATE compliances 
                SET regulatory_body = %s, compliance_detail = %s, frequency = %s, 
                    doc_ref_no = %s, consent_valid_from = %s, valid_upto = %s, remarks = %s 
                WHERE id = %s
            """, (regulatory_body, compliance_detail, frequency, doc_ref_no, consent_valid_from, valid_upto, remarks, id))
            
            conn.commit()
            flash('Compliance Updated Successfully', 'success')
            return redirect(url_for('index'))

        # Fetch the existing compliance record to populate the edit form
        cur.execute("SELECT * FROM compliances WHERE id = %s", (id,))
        compliance = cur.fetchone()
        
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('index'))
    finally:
        cur.close()
        conn.close()
    
    return render_template('edit.html', compliance=compliance)

# Route to delete compliance
@app.route('/delete/<string:id>', methods=['POST'])
def delete_compliance(id):
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("DELETE FROM compliances WHERE id = %s", (id,))
        conn.commit()
        flash('Compliance Deleted Successfully', 'success')
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('index'))

# Route for compliance details with pagination
@app.route('/compliance_details', methods=['GET', 'POST'])
def compliance_details():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        page = request.args.get('page', 1, type=int)  # Get the current page, default is 1
        per_page = 5  # Number of records per page

        regulatory_body = None
        if request.method == 'POST':
            regulatory_body = request.form['regulatory_body']
            
            # Fetch compliance details for the selected regulatory body with pagination
            cur.execute("SELECT COUNT(*) FROM compliances WHERE regulatory_body = %s", (regulatory_body,))
            total_compliances = cur.fetchone()[0]

            cur.execute("""
                SELECT * FROM compliances 
                WHERE regulatory_body = %s 
                LIMIT %s OFFSET %s
            """, (regulatory_body, per_page, (page - 1) * per_page))
            selected_compliances = cur.fetchall()

            # Fetch distinct regulatory bodies for the dropdown
            cur.execute("SELECT DISTINCT regulatory_body FROM compliances")
            regulatory_bodies = cur.fetchall()
            
            cur.close()
            return render_template(
                'compliance_details.html', 
                selected_compliances=selected_compliances, 
                regulatory_bodies=regulatory_bodies, 
                regulatory_body=regulatory_body, 
                page=page, 
                total_pages=(total_compliances // per_page) + (1 if total_compliances % per_page > 0 else 0)
            )

        # For GET request, fetch distinct regulatory bodies for the dropdown
        cur.execute("SELECT DISTINCT regulatory_body FROM compliances")
        regulatory_bodies = cur.fetchall()
        
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        return redirect(url_for('index'))
    finally:
        cur.close()
        conn.close()
    
    return render_template('compliance_details.html', regulatory_bodies=regulatory_bodies)

if __name__ == "__main__":
    app.run(debug=True)
