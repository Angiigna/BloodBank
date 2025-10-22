#step -2 import the create_app we just made and use it 
from website import create_app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)#only run server if we run main
