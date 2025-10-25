from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
# Create your views here.
from Remote_User.models import ClientRegister_Model,predict_climate_change_impact,detection_ratio,detection_accuracy

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def Register1(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city)

        return render(request, 'RUser/Register1.html')
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def Prediction_Of_Climate_Change_Impact(request):
    if request.method == "POST":

        if request.method == "POST":

            Fid= request.POST.get('Fid')
            CDate= request.POST.get('CDate')
            Precipitation= request.POST.get('Precipitation')
            Humidity= request.POST.get('Humidity')
            WindSpeed= request.POST.get('WindSpeed')
            WeatherCondition= request.POST.get('WeatherCondition')
            AvgTemp= request.POST.get('AvgTemp')
            AvgTempUncertainty= request.POST.get('AvgTempUncertainty')
            City= request.POST.get('City')
            Country= request.POST.get('Country')
            Latitude= request.POST.get('Latitude')
            Longitude= request.POST.get('Longitude')
            Season= request.POST.get('Season')
            Crop= request.POST.get('Crop')


        data = pd.read_csv("Datasets.csv", encoding='latin-1')

        def apply_response(Label):
            if (Label == 0):
                return 0  # Good
            elif (Label == 1):
                return 1  # Bad

        data['Results'] = data['Label'].apply(apply_response)

        x = data['Fid']
        y = data['Results']
        cv = CountVectorizer()

        x = cv.fit_transform(x)

        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
        X_train.shape, X_test.shape, y_train.shape


        print("Logistic Regression")

        from sklearn.linear_model import LogisticRegression

        reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('logistic', reg))

        print("MLPClassifier")
        from sklearn.neural_network import MLPClassifier
        mlpc = MLPClassifier().fit(X_train, y_train)
        y_pred = mlpc.predict(X_test)
        testscore_mlpc = accuracy_score(y_test, y_pred)
        accuracy_score(y_test, y_pred)
        print(accuracy_score(y_test, y_pred))
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('MLPClassifier', mlpc))

        from sklearn.ensemble import GradientBoostingClassifier
        clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0).fit(
            X_train,
            y_train)
        clfpredict = clf.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, clfpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, clfpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, clfpredict))
        models.append(('GradientBoostingClassifier', clf))


        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        Fid1 = [Fid]
        vector1 = cv.transform(Fid1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = pred.replace("]", "")

        prediction = int(pred1)

        if prediction == 0:
            val = 'Good'
        elif prediction == 1:
            val = 'Bad'

        print(prediction)
        print(val)

        predict_climate_change_impact.objects.create(
        Fid=Fid,
        CDate=CDate,
        Precipitation=Precipitation,
        Humidity=Humidity,
        WindSpeed=WindSpeed,
        WeatherCondition=WeatherCondition,
        AvgTemp=AvgTemp,
        AvgTempUncertainty=AvgTempUncertainty,
        City=City,
        Country=Country,
        Latitude=Latitude,
        Longitude=Longitude,
        Season=Season,
        Crop=Crop,
        Prediction=val)

        return render(request, 'RUser/Prediction_Of_Climate_Change_Impact.html',{'objs': val})
    return render(request, 'RUser/Prediction_Of_Climate_Change_Impact.html')



