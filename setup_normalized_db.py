from db_config_normalized import init_database, test_connection

if __name__ == "__main__":
    print("🚀 Setting up normalized database...")
    
    if test_connection():
        print("✅ Database connection successful!")
        try:
            init_database()
            print("✅ Database setup completed successfully!")
            print("\n📊 Database Structure:")
            print("- locations: Menyimpan data lokasi")
            print("- criteria: Menyimpan kriteria penilaian")
            print("- evaluations: Menyimpan nilai penilaian")
            print("- calculation_results: Cache hasil perhitungan")
            print("\n🚀 Ready to run: python main_normalized.py")
        except Exception as e:
            print(f"❌ Database setup failed: {e}")
    else:
        print("❌ Database connection failed!")
        print("💡 Please check your .env configuration")
