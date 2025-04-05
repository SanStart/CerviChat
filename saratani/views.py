import json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
import cv2
import numpy as np
from skimage.transform import resize
from keras.models import load_model
from saratani.models import Prediction
from .forms import PredictionForm
from django.contrib.auth.decorators import login_required
import io
from tf_explain.core.grad_cam import GradCAM
from django.http import FileResponse
from reportlab.pdfgen import canvas
import os
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from keys.environs import keys,feature_names
@login_required
def predict_paps(request,image_id):
    try:
        patient_test = Prediction.objects.get(ide=image_id)
        img_path = str(patient_test.image.url)[1:]
        img = cv2.imread(img_path)
        img = resize(img, (64,64,3))
        X = np.asarray(img).astype('float32')
        model = load_model('static/saratani_predictive_model.h5')
        prediction = model.predict(X.reshape((1, 64, 64, 3)))
        print(prediction)
        target_values = list(prediction[0])
        _targets = {'NSI': 0,
                    'AK': 1,
                    'AD': 2,
                    'BM': 3,
                    'NP': 4,
                    'NSD': 5,
                    'ALD': 6,
                    'ACIS': 7,
                    'AMD': 8,
                    'NC': 9, 
                    'NS': 10,
                    'NI': 11}
        targets = list(_targets.keys())
        def stringfy_response(my_response):
            return my_response.replace("_"," ").title()

        response = dict()
        for i in range(0, len(targets)):
            response[str(targets[i])] = float(target_values[i])
        sorted_results = dict(sorted(response.items(), key=lambda item: item[1]))
        # high_prob = dict(sorted(response.items(), key=lambda item: item[1]))
        patient_test.results = json.dumps(sorted_results)
        initial_ft = stringfy_response(str(list(sorted_results.keys())[-1]))
        patient_test.feature   = initial_ft
        patient_test.f_name = feature_names[initial_ft.upper()]
        patient_test.f_value   = str(round(sorted_results[list(sorted_results.keys())[-1]],4)*100)[:5]
        patient_test.predicted = True
        patient_test.save()
        messages.success(request, 'Predicted successfully!')
        return redirect("/")
    except:
        messages.warning(request, 'An error occured.')
        return redirect("/")


@login_required
def predictions(request):
    context = dict()
    if request.method == "POST":
        form_data = PredictionForm(request.POST, request.FILES)
        if form_data.is_valid():
            form_data.instance.user = request.user
            form_data.save()

    try:
        context['predictions'] = Prediction.objects.filter(user=request.user)
        context['available']   = True
        context['page_is_predictions'] = True
        context['form'] = PredictionForm
    except:
        context['available']   = False 
        context['page_is_predictions'] = True
        context['form'] = PredictionForm
    
    return render(request, 'saratani/predictions.html', context)

@login_required
def delete_prediction(request, ide):
    obj = Prediction.objects.get(ide=ide)
    if obj.user == request.user:
        messages.success(request, 'Deleted successfully!')
        print(obj.image.url[1:])
        os.remove(obj.image.url[1:])
        obj.delete()
    else:
        messages.warning(request, 'Error Occured!')
    return redirect("/")
@login_required
def report(request, ide):
    buffer    = io.BytesIO()
    receipt   = canvas.Canvas(buffer)
    obj = Prediction.objects.get(ide=ide)
    receipt.setLineWidth(.6)
    receipt.setFont('Courier', 20)
    receipt.drawString(95, 755,'SARATANI AI PAPS SMEAR PREDICTIONS')
    receipt.drawString(220, 740,'-----•••-----')
    receipt.setFont('Courier', 17)
    receipt.drawString(225, 728,"PATIENT REPORT")
    receipt.drawImage(f'static/assets/img/saratani.png', 180, 560, width=259.91031390134526, height=120)
    receipt.setDash(2,3)

    #
    receipt.setFont('Courier', 11)
    receipt.drawString(390, 535, "{}".format(obj.date_scanned.strftime("%b %d %Y,%H:%M")))
    receipt.line(70, 530, 520, 530)
    receipt.drawString(70, 515, "PATIENT NAME")
    receipt.drawString(410, 515, f'{obj.patient_name}'.upper())

    receipt.setFont('Courier', 11)
    if obj.predicted:
        receipt.drawString(70, 500, "DOCTOR'S ID")
        receipt.drawString(410, 500, f'{request.user.username}'.upper())

    receipt.line(130, 480, 520, 480)
    receipt.drawString(150, 470,'PARTICULARS')
    receipt.drawString(350, 470,'DETAILS')
    receipt.line(130, 465, 520, 465)

    receipt.drawString(150, 450, "HIGHEST FEATURE")
    receipt.drawString(350, 450, f'{obj.f_name}')

    receipt.drawString(150, 430, "PROBABILITY")
    receipt.drawString(350, 430, f'{obj.f_value}%')


    receipt.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=f'{obj.patient_name.upper()}-{obj.date_scanned.strftime("%b %d %Y,%H:%M")}.pdf')


@login_required
def analysis(request, id):
    context = dict()
    prediction = Prediction.objects.get(ide=id)
    context['prediction'] = prediction
    results = json.loads(prediction.results)
    features , important_scores = list(results.keys()), list(results.values())

    # Clear the figure
    plt.clf()


    scores = [float(str(round(number,4)*100)[:5]) for number in important_scores]

    table_of_results = list()
    for i in range(0, len(scores)):
        if scores[i] > 0:
            obj = dict()
            obj['initial'] = features[i]
            obj['score'] = scores[i]
            obj['name'] = feature_names[features[i]]
            table_of_results.append(obj)

    reversed_results = list(reversed(table_of_results))
    context['results'] = reversed_results
    context['feature_names'] = feature_names
    context['high_prob'] = reversed_results[0]

    # print(reversed_results[0])

    #  create a heat map here
    img_path = str(prediction.image.url)[1:]
    # img_path = '/home/kalokola/saratani/media/predictions/paps.jpeg'
    # Create a GradCAM object
    explainer = GradCAM()

    # Choose a target class index (e.g., the index corresponding to the class you want to localize)
    target_class_index = 2  # Change this to the index of the class you want to visualize

    # Load and preprocess your image
    orig = cv2.imread(img_path)
    orig_resized = resize(orig, (64,64,3))
    img = cv2.imread(img_path)
    img = resize(img, (64, 64, 3))
    img = np.asarray(img).astype('float32')
    img = img.reshape((1, 64, 64, 3))

    saratani_model = load_model('static/saratani_predictive_model.h5')

    # Generate Grad-CAM heatmap
    grid = explainer.explain(validation_data=(img, None), model=saratani_model, class_index=target_class_index)
    # Normalize the heatmap values to [0, 1]
    heatmap = grid[0] / np.max(grid[0])

    
    # Resize the heatmap to match the original image dimensions
    heatmap = cv2.resize(heatmap, (orig_resized.shape[1], orig_resized.shape[1]))

    # Convert heatmap to RGB format
    heatmap = cv2.applyColorMap(np.uint8(255 * heatmap), cv2.COLORMAP_JET)
    plt.imshow(heatmap)
    # plt.xlabel('Features')
    # plt.ylabel('Importance (%ge)')
    # plt.title('FEATURE IMPORTANCE HEATMAP')
    buffer = io.BytesIO()

    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    context['graphic'] = graphic
    return render(request, 'saratani/results.html', context)