from flask import Flask, render_template, request, send_file
import pandas as pd
import os
from sqlalchemy import create_engine
from datetime import datetime
from supabase import create_client, Client

# Flask app setup
app = Flask(__name__)

# Supabase setup
SUPABASE_URL = "https://dvfjspdpfqwsjxinkmjr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR2ZmpzcGRwZnF3c2p4aW5rbWpyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA4NTA3MTksImV4cCI6MjA1NjQyNjcxOX0.ZA8pk87iOiYkVs68y6p2h6BZ5Vf4VxHz1ZkoR08zBfE"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Define database connection
DATABASE_URL = "postgresql://postgres:Smp-mcp_060809@db.dvfjspdpfqwsjxinkmjr.supabase.co:5432/postgres"
engine = create_engine(DATABASE_URL)

# Create the data entry form route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        data = {
            "cattle": request.form.get("cattle", type=int),
            "buffalo": request.form.get("buffalo", type=int),
            "sheep_goat_doze": request.form.get("sheep_goat_doze", type=int),
            "sheep_goat_dust": request.form.get("sheep_goat_dust", type=int),
            "sheep_goat_treat": request.form.get("sheep_goat_treat", type=int),
            "horse": request.form.get("horse", type=int),
            "camel": request.form.get("camel", type=int),
            "other": request.form.get("other", type=int),
            "endo": request.form.get("endo", type=int),
            "ecto": request.form.get("ecto", type=int),
            "drug_distribution": request.form.get("drug_distribution", type=int),
            "male_sc": request.form.get("male_sc", type=int),
            "male_st": request.form.get("male_st", type=int),
            "male_obc": request.form.get("male_obc", type=int),
            "female_sc": request.form.get("female_sc", type=int),
            "female_st": request.form.get("female_st", type=int),
            "female_obc": request.form.get("female_obc", type=int),
        }

        # Insert into Supabase
        supabase.table("data_entries").insert(data).execute()
        return "Data Submitted Successfully!"

    return render_template("index.html")

# Generate Master Excel Sheet
@app.route("/generate-excel")
def generate_excel():
    # Fetch data from Supabase
    response = supabase.table("data_entries").select("*").execute()
    records = response.data

    if not records:
        return "No data available."

    # Convert to Pandas DataFrame
    df = pd.DataFrame(records)
    filename = f"master_sheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = os.path.join("static", filename)
    
    # Save to Excel
    df.to_excel(filepath, index=False)
    return send_file(filepath, as_attachment=True)

# Run app
if __name__ == "__main__":
    app.run(debug=True)
