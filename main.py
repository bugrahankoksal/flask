from website import create_app

app = create_app()

# sadece bu sayfayı direkt olarak calistirirsan app calisir. Baska bi dosyadan
# bu main dosyasını import edersen app calismasin diye bu if sorgusu gerekiyor
if __name__ == "__main__":
    app.run(debug=True)
