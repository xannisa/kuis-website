from apps.__init__ import app
import apps.auth
import apps.kuis
import apps.leaderboard 
import apps.home

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)