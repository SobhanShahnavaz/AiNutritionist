from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import ExercieMaps,DietMaps
import os
import joblib
import numpy as np
import pandas as pd

def calculate_bmi(weight_kg, height_cm):
    if height_cm <= 0:
        raise ValueError("قد باید عددی بزرگتر از صفر باشد.")
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)
def StandExecisePredictor(Profile):
    MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
    XGBMODEL = os.path.join(MODEL_DIR, "XGBExercise.pkl")
    
    if Profile.count:
        ExerciseModel = joblib.load(XGBMODEL)
        ExeciseSet = ExerciseModel.predict(Profile)
        ExLabel = int(ExeciseSet[0] if isinstance(ExeciseSet, tuple) else ExeciseSet)
        return ExLabel
    
        

def HomePage(request):
    template = loader.get_template('Index.html')
    return HttpResponse(template.render())

def About(request):
    template = loader.get_template('About.html')
    return HttpResponse(template.render())

def ExerciseForm(request):
    template = loader.get_template('ExerciseForm.html')
    return HttpResponse(template.render())

def NutritionForm(request):
    template = loader.get_template('NutritionForm.html')
    return HttpResponse(template.render())

def DietForm(request):
    template = loader.get_template('DietForm.html')
    return HttpResponse(template.render())

def NutritionPredict(request):
    MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
    ECDNMODEL_PATH = os.path.join(MODEL_DIR, "MlrEDCNV2.pkl")
    ECDNSCALER_PATH = os.path.join(MODEL_DIR, "scalerMlrEDCNV2.pkl")
    CARBOHYDRATEMODEL_PATH = os.path.join(MODEL_DIR, "MlrCarbohydrate.pkl")
    CARBOHYDRATESCALER_PATH = os.path.join(MODEL_DIR, "scalerMlrCarbohydrate.pkl")
    TOTALFIBERMODEL_PATH = os.path.join(MODEL_DIR, "MlrTotalFiber.pkl")
    TOTALFIBERSCALER_PATH = os.path.join(MODEL_DIR, "scalerMlrTotalFiber.pkl")
    PROTEINMODEL_PATH = os.path.join(MODEL_DIR, "MlrProtein.pkl")
    PROTEINSCALER_PATH = os.path.join(MODEL_DIR, "scalerMlrProtein.pkl")
    if request.GET :
        ECDNmodel = joblib.load(ECDNMODEL_PATH)
        ECDNscaler = joblib.load(ECDNSCALER_PATH)
        CARBOHYDRATEmodel = joblib.load(CARBOHYDRATEMODEL_PATH)
        CARBOHYDRATEscaler = joblib.load(CARBOHYDRATESCALER_PATH)
        TOTALFIBERmodel = joblib.load(TOTALFIBERMODEL_PATH)
        TOTALFIBERscaler = joblib.load(TOTALFIBERSCALER_PATH)
        PROTEINmodel = joblib.load(PROTEINMODEL_PATH)
        PROTEINscaler = joblib.load(PROTEINSCALER_PATH)


        Gender = int(request.GET.get("Gender", 0)),
        Age = int(request.GET.get("Age", 0)),
        Height = float(request.GET.get("Height", 0)),
        Weight = float(request.GET.get("Weight", 0)),
        Activitylevel = float(request.GET.get("Activity", 0))
        Gender = float(Gender[0] if isinstance(Gender, tuple) else Gender)
        Age = float(Age[0] if isinstance(Age, tuple) else Age)
        Height = float(Height[0] if isinstance(Height, tuple) else Height)
        Weight = float(Weight[0] if isinstance(Weight, tuple) else Weight)
        Activitylevel = float(Activitylevel[0] if isinstance(Activitylevel, tuple) else Activitylevel)
        BMI = calculate_bmi(Weight, Height)
        BSA = np.sqrt((Height* Weight) / 3600)
        AW = (Age* Weight) 
        PAW = (Activitylevel* Weight) 
        PAH = (Activitylevel* Height) 
        BSAPA = (BSA* Activitylevel) 
        SPA = (Gender* Activitylevel) 
        BSAPAS = (BSA* Activitylevel* Gender) 



        ECDNscaled_input = ECDNscaler.transform([[Gender, Age, Height, Weight, Activitylevel, BSA , AW ,PAW,PAH,BSAPA,SPA,BSAPAS]])
        ECDNprediction = ECDNmodel.predict(ECDNscaled_input)
        ECDN = ECDNprediction[0]
       
        if Age <= 3:
            FATMIN = 0.3 * (ECDN/ 9)
            FATMAX = 0.4 *(ECDN/ 9)
        elif Age > 3 and Age <= 18:
            FATMIN = (25 / 100) *(ECDN/ 9)
            FATMAX = (35 / 100) *(ECDN/ 9)
        else:
            FATMIN = (20 / 100) *(ECDN/ 9)
            FATMAX = (35 / 100) *(ECDN/ 9)
        CARBOHYDRATEMIN = (45 / 100) *(ECDN/ 4)
        CARBOHYDRATEMAX = (65 / 100) *(ECDN/ 4)
        TOTALFIBERscaled_input = TOTALFIBERscaler.transform([[Gender, Age, Height, Weight, Activitylevel, BMI]])
        TOTALFIBERprediction = TOTALFIBERmodel.predict(TOTALFIBERscaled_input)
        TOTALFIBER = TOTALFIBERprediction[0]
        PROTEINscaled_input = PROTEINscaler.transform([[Gender, Age, Height, Weight, Activitylevel, BMI]])
        PROTEINprediction = PROTEINmodel.predict(PROTEINscaled_input)
        PROTEIN = PROTEINprediction[0]
        if Gender == 1:
            TextGender = "مذکر"
        elif Gender == 0: 
            TextGender = "مونث"
        if Activitylevel == 1:
            TextActivitylevel = "غیرفعال"
        elif Activitylevel == 1.4: 
            TextActivitylevel = "کمی فعال"
        elif Activitylevel == 1.6:
            TextActivitylevel = "فعال"
        elif Activitylevel == 1.9: 
            TextActivitylevel = "بسیار فعال"
        template = loader.get_template('NutritionPredict.html')
        context = {
        'ECDN': ECDN,
        'FATMIN': FATMIN,
        'FATMAX': FATMAX,
        'CARBOHYDRATEMIN': CARBOHYDRATEMIN,
        'CARBOHYDRATEMAX': CARBOHYDRATEMAX,
        'TOTALFIBER': TOTALFIBER,
        'PROTEIN': PROTEIN,
        'Gender':TextGender ,
        'Age':Age  ,
        'Height':Height ,
        'Weight':Weight ,
        'Activitylevel':TextActivitylevel,
        'BMI':BMI
        }
        return HttpResponse(template.render(context, request))
    else :
        return redirect('NutritionForm')
    
def ExercisePredict(request):
    MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
    XGBMODEL = os.path.join(MODEL_DIR, "XGBExercise.pkl")
    if request.GET :
        ExerciseModel = joblib.load(XGBMODEL)

        Gender = int(request.GET.get("Gender", 0)),
        Age = int(request.GET.get("Age", 0)),
        Height = float(request.GET.get("Height", 0)),
        Weight = float(request.GET.get("Weight", 0)),
        Level = float(request.GET.get("Level", 0)),
        Diabetes = float(request.GET.get("Diabetes", 0)),
        Hypertension = float(request.GET.get("Hypertension", 0)),
        Gender = float(Gender[0] if isinstance(Gender, tuple) else Gender)
        Age = int(Age[0] if isinstance(Age, tuple) else Age)
        Height = float(Height[0] if isinstance(Height, tuple) else Height)
        Weight = float(Weight[0] if isinstance(Weight, tuple) else Weight)
        Level = int(Level[0] if isinstance(Level, tuple) else Level)
        Diabetes = int(Diabetes[0] if isinstance(Diabetes, tuple) else Diabetes)
        Hypertension = int(Hypertension[0] if isinstance(Hypertension, tuple) else Hypertension)
        BMI = calculate_bmi(Weight, Height)
        if BMI < 18.5:
            RealLevel = 0
        elif BMI < 25:
            RealLevel = 1
        elif BMI < 30:
            RealLevel = 2
        else:
            RealLevel = 3
        if Level == 4:
            Level = RealLevel
        if Level == RealLevel:
            IsLevel = 1
        else:
            IsLevel = 0

        
        UserProfile = {
            'Sex': [Gender],          
            'Hypertension': [Hypertension], 
            'Diabetes': [Diabetes],     
            'Level': [RealLevel],        
            'Age': [Age],         
            'Height': [Height],     
            'Weight': [Weight]       
        }

        UserDataFrame = pd.DataFrame(UserProfile)
        ExeciseSet = ExerciseModel.predict(UserDataFrame)
        ExLabel = int(ExeciseSet[0] if isinstance(ExeciseSet, tuple) else ExeciseSet)
        
        Map = ExercieMaps.objects.get(Label=ExLabel)
        SetNumber = Map.Label +1
        if Gender == 0:
            TextGender = "مذکر"
        elif Gender == 1: 
            TextGender = "مونث"
        if Level == 0:
            TextLevel = "دارای کسر وزن"
        elif Level == 1: 
            TextLevel = "عادی"
        elif Level == 2:
            TextLevel = "اضافه وزن"
        elif Level == 3: 
            TextLevel = "فربه"
        if RealLevel == 0:
            TextRealLevel = "دارای کسر وزن"
        elif RealLevel == 1: 
            TextRealLevel = "عادی"
        elif RealLevel == 2:
            TextRealLevel = "اضافه وزن"
        elif RealLevel == 3: 
            TextRealLevel = "فربه"
        if Diabetes == 0 and Hypertension ==0:
            Diseases = "بدون بیماری."
        elif Diabetes == 1 and Hypertension ==0:
            Diseases = "دیابت."
        elif Diabetes == 0 and Hypertension ==1:
            Diseases = "فشار خون."
        elif Diabetes == 1 and Hypertension ==1:
            Diseases = "دیابت، فشارخون."
            
        template = loader.get_template('ExercisePredict.html')
        context = {
        'SetNumber' : SetNumber,
        'Map':Map,
        'Gender':TextGender ,
        'Age':Age  ,
        'Height':Height ,
        'Weight':Weight ,
        'BMI':BMI ,
        'Level':TextLevel ,
        'RealLevel':TextRealLevel,
        'IsLevel':IsLevel ,
        'Diabetes':Diabetes ,
        'Hypertension':Hypertension ,
        'Diseases' : Diseases,
        
        }
        return HttpResponse(template.render(context, request))
    else :
        return redirect('ExerciseForm')

def DietPredict(request):
    MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
    XGBDMODEL = os.path.join(MODEL_DIR, "XGBdiet.pkl")
    if request.GET :
        DietModel = joblib.load(XGBDMODEL)

        Gender = int(request.GET.get("Gender", 0)),
        Age = int(request.GET.get("Age", 0)),
        Height = float(request.GET.get("Height", 0)),
        Weight = float(request.GET.get("Weight", 0)),
        Level = float(request.GET.get("Level", 0)),
        ExerciseLabel = float(request.GET.get("Exercise_Label", 0)),
        Diabetes = float(request.GET.get("Diabetes", 0)),
        Hypertension = float(request.GET.get("Hypertension", 0)),
        Gender = float(Gender[0] if isinstance(Gender, tuple) else Gender)
        Age = int(Age[0] if isinstance(Age, tuple) else Age)
        Height = float(Height[0] if isinstance(Height, tuple) else Height)
        Weight = float(Weight[0] if isinstance(Weight, tuple) else Weight)
        Level = int(Level[0] if isinstance(Level, tuple) else Level)
        ExerciseLabel = int(ExerciseLabel[0] if isinstance(ExerciseLabel, tuple) else ExerciseLabel)
        Diabetes = int(Diabetes[0] if isinstance(Diabetes, tuple) else Diabetes)
        Hypertension = int(Hypertension[0] if isinstance(Hypertension, tuple) else Hypertension)
        BMI = calculate_bmi(Weight, Height)
        if BMI < 18.5:
            RealLevel = 0
        elif BMI < 25:
            RealLevel = 1
        elif BMI < 30:
            RealLevel = 2
        else:
            RealLevel = 3
        if Level == 4:
            Level = RealLevel
        if Level == RealLevel:
            IsLevel = 1
        else:
            IsLevel = 0
        UnhealthyScore =(Hypertension*5) * (ExerciseLabel +1 ) + (Level * 2) 
        if ExerciseLabel == 404:
            UserTempProfile = {
            'Sex': [Gender],          
            'Hypertension': [Hypertension], 
            'Diabetes': [Diabetes],     
            'Level': [RealLevel],        
            'Age': [Age],         
            'Height': [Height],     
            'Weight': [Weight]       
            }
            UserTempDataFrame = pd.DataFrame(UserTempProfile)
            ExerciseLabel = StandExecisePredictor(UserTempDataFrame)
        
        UserProfile = {
            'Sex': [Gender],          
            'Hypertension': [Hypertension], 
            'Diabetes': [Diabetes],     
            'Level': [RealLevel],        
            'Age': [Age],
            'BMI':[BMI],         
            'Height': [Height],     
            'Weight': [Weight],
            'Exercises_Label': [ExerciseLabel],
            'UnhealthyScore': [UnhealthyScore]

        }

        UserDataFrame = pd.DataFrame(UserProfile)

        DietSet = DietModel.predict(UserDataFrame)
        DietLabel = int(DietSet[0] if isinstance(DietSet, tuple) else DietSet)
        
        Map = DietMaps.objects.get(Label=DietLabel)
        MapEx = ExercieMaps.objects.get(Label=ExerciseLabel)
        SetNumber = Map.Label +1

        if Gender == 0:
            TextGender = "مذکر"
        elif Gender == 1: 
            TextGender = "مونث"
        if Level == 0:
            TextLevel = "دارای کسر وزن"
        elif Level == 1: 
            TextLevel = "عادی"
        elif Level == 2:
            TextLevel = "اضافه وزن"
        elif Level == 3: 
            TextLevel = "فربه"
        if RealLevel == 0:
            TextRealLevel = "دارای کسر وزن"
        elif RealLevel == 1: 
            TextRealLevel = "عادی"
        elif RealLevel == 2:
            TextRealLevel = "اضافه وزن"
        elif RealLevel == 3: 
            TextRealLevel = "فربه"
        if ExerciseLabel == 0:
            TextExerciseLabel = "ست یک"
        elif ExerciseLabel == 1: 
            TextExerciseLabel = "ست دو"
        elif ExerciseLabel == 2:
            TextExerciseLabel = "ست سه"
        elif ExerciseLabel == 3: 
            TextExerciseLabel = "ست چهار"
        elif ExerciseLabel == 4: 
            TextExerciseLabel = "ست پنج"
        if Diabetes == 0 and Hypertension ==0:
            Diseases = "بدون بیماری."
        elif Diabetes == 1 and Hypertension ==0:
            Diseases = "دیابت."
        elif Diabetes == 0 and Hypertension ==1:
            Diseases = "فشار خون."
        elif Diabetes == 1 and Hypertension ==1:
            Diseases = "دیابت، فشارخون."
            
        template = loader.get_template('DietPredict.html')
        context = {
        'SetNumber' : SetNumber,
        'Map':Map,
        'Gender':TextGender ,
        'Age':Age  ,
        'Height':Height ,
        'Weight':Weight ,
        'BMI':BMI ,
        'Level':TextLevel ,
        'RealLevel':TextRealLevel,
        'IsLevel':IsLevel ,
        'Diabetes':Diabetes ,
        'ExerciseLabel': ExerciseLabel,
        'TextExerciseLabel':TextExerciseLabel,
        'Hypertension':Hypertension ,
        'Diseases' : Diseases,
        'MapEx':MapEx,
        
        }
        return HttpResponse(template.render(context, request))
    else :
        return redirect('DietForm')