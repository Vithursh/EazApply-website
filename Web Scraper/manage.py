from app import read_csv_and_store_in_database, db, data

app = read_csv_and_store_in_database('File Data/linkedin-jobs.csv')

@app.cli.command("reset_db")
def reset_db():
    """Drop existing tables and create new ones."""
    with app.app_context():
        #db.create_all()
        # Now you can insert data into the data table
        record = data(title='Software Engineer', company='Instacart', location='Toronto, Ontario, Canada', applyLink='https://ca.linkedin.com/jobs/view/software-engineer-at-instacart-3778290848?refId=GyI2rASdmSHPlL%2FDyX0Z1g%3D%3D&trackingId=YpL%2FHHwPS0rpLgLyhPa3Zg%3D%3D&position=1&pageNum=0&trk=public_jobs_jserp-result_search-card')
        db.session.add(record)
        db.session.commit()

        print("Database tables reset.")

if __name__ == "__main__":
    app.run()
