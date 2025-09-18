from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import datetime
import numpy as np

from sklearn.ensemble import RandomForestClassifier
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
# Create your views here.
from Remote_User.models import ClientRegister_Model,cardiac_arrest_prediction,detection_ratio,detection_accuracy

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

def Add_DataSet_Details(request):

    return render(request, 'RUser/Add_DataSet_Details.html', {"excel_data": ''})


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


def Predict_Cardiac_Arrest_Type(request):
    if request.method == "POST":

        if request.method == "POST":

            Fid= request.POST.get('Fid')
            Age_In_Days= request.POST.get('Age_In_Days')
            Sex= request.POST.get('Sex')
            ChestPainType= request.POST.get('ChestPainType')
            RestingBP= request.POST.get('RestingBP')
            RestingECG= request.POST.get('RestingECG')
            MaxHR= request.POST.get('MaxHR')
            ExerciseAngina= request.POST.get('ExerciseAngina')
            Oldpeak= request.POST.get('Oldpeak')
            ST_Slope= request.POST.get('ST_Slope')
            slp= request.POST.get('slp')
            caa= request.POST.get('caa')
            thall= request.POST.get('thall')


        data = pd.read_csv("Datasets.csv", encoding='latin-1')

        def apply_results(status):
            if (status == 0):
                return 0  # No Cardiac Arrest Found
            elif (status == 1):
                return 1  # Cardiac Arrest Found

        data['Results'] = data['HeartDisease'].apply(apply_results)

        x = data['Fid']
        y = data['Results']


        cv = CountVectorizer()

        x = cv.fit_transform(x)

        print(x)
        print("Y")
        print(y)

        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
        X_train.shape, X_test.shape, y_train.shape

        print("Artificial Neural Network (ANN)")

        from sklearn.neural_network import MLPClassifier
        mlpc = MLPClassifier().fit(X_train, y_train)
        y_pred = mlpc.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('MLPClassifier', mlpc))

        # SVM Model
        print("SVM")
        from sklearn import svm

        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        predict_svm = lin_clf.predict(X_test)
        svm_acc = accuracy_score(y_test, predict_svm) * 100
        print(svm_acc)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, predict_svm))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, predict_svm))
        models.append(('svm', lin_clf))

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


        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        Fid1 = [Fid]
        vector1 = cv.transform(Fid1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = str(pred.replace("]", ""))

        prediction = int(pred1)

        if prediction == 0:
            val = 'No Cardiac Arrest Found'
        elif prediction == 1:
            val = 'Cardiac Arrest Found'

        print(prediction)
        print(val)

        cardiac_arrest_prediction.objects.create(
        Fid=Fid,
        Age_In_Days=Age_In_Days,
        Sex=Sex,
        ChestPainType=ChestPainType,
        RestingBP=RestingBP,
        RestingECG=RestingECG,
        MaxHR=MaxHR,
        ExerciseAngina=ExerciseAngina,
        Oldpeak=Oldpeak,
        ST_Slope=ST_Slope,
        slp=slp,
        caa=caa,
        thall=thall,
        Prediction=val)

        return render(request, 'RUser/Predict_Cardiac_Arrest_Type.html',{'objs': val})
    return render(request, 'RUser/Predict_Cardiac_Arrest_Type.html')



