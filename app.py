# save this as app.py
from flask import Flask, request, render_template, request
import pickle
import requests

with open("models/movies_list.pkl","rb") as f:
     movies = pickle.load(f)

with open("models/similarity.pkl","rb") as fo:
     similarity = pickle.load(fo)
#movies = pickle.load(open('models/movies_list.pkl', 'rb'))
#similarity = pickle.load(open('models/similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse= True, key=lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)

    return recommended_movies_name, recommended_movies_poster

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")


@app.route("/feedback")
def feed():
	return render_template("feedback.html")

@app.route("/feedback", methods=["GET", "POST"])
def receive():
	firstname =  request.form["firstname"]
	lastname = request.form["lastname"]
	rating = request.form["Rating"]
	feed = request.form["feed"]
	msg2 = " Hurry! " + firstname + " " +  lastname + " Your Feedback has been sent to Project Owner i.e to Tejas More " + " "
	msg3 = "Rating : " + rating + " " + " , " + " "+ "Feedback :  "+ feed 
	f = open("FEEDBACK.txt", "a")
	f.writelines(["\nNew Feedback is Here : " + "\n" "\nFIRST NAME : " + firstname , "\nLAST NAME : " + lastname, "\nRating : " + rating + " " + "\nFeedback :  "+ feed + " \n " ])
	f.close()

	return render_template("feedback.html", msg2= msg2, msg3=msg3)


@app.route('/recommendation', methods = ['GET', 'POST'])
def recommendation():
    movie_list = movies['title'].values
    status = False
    if request.method == "POST":
        try:
            if request.form:
                movies_name = request.form['movies']
                print(movies_name)
                recommended_movies_name, recommended_movies_poster = recommend(movies_name)
                print(recommended_movies_name)
                print(recommended_movies_poster)
                status = True

                return render_template("prediction.html", movies_name = recommended_movies_name, poster = recommended_movies_poster, movie_list = movie_list, status = status)




        except Exception as e:
            error = {'error': e}
            return render_template("prediction.html",error = error, movie_list = movie_list, status = status)

    else:
        return render_template("prediction.html", movie_list = movie_list, status = status)




    






if __name__ == '__main__':
    app.debug = True
    app.run()
    