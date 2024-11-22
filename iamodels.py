import threading
from queue import Queue
from transformers import pipeline
import json
import os
import pickle

status = {
	"1":"Negativo",
	"2":"Negativo",
	"3":"Neutro",
	"4":"Positivo",
	"5":"Positivo"
}

def process_input(inp, features, target, status, analizador, queue):
	results = analizador(inp[features])
	for r in results:
		res = r['label'].split(" ")[0]
	inp[target] = status[res]
	queue.put(inp)

def AnalitysTrain(model,ruta):

	try:analizador = pipeline(model[0], model=model[1],device=0)
	except:analizador = pipeline(model[0], model=model[1])

	model_name = f"{ruta}/model.pkl"

	with open(model_name, 'wb') as f:
		pickle.dump(analizador, f)

	print(f"Modelo guardado en {model_name}")

def AnalitysMain(features,target,data,ruta,output_filename,filters,num_threads = 3):
	queue = Queue()
	threads = []

	with open(f"{ruta}/model.pkl", 'rb') as f:
		analizador = pickle.load(f)

	for inp in data:
		thread = threading.Thread(target=process_input, args=(inp.copy(), features, target, status, analizador, queue))
		threads.append(thread)
		thread.start()

	response = []

	for _ in range(len(data)):
		response.append(queue.get())

	for thread in threads:
		thread.join()
	
	file_out = f"{ruta}/{output_filename}"
	with open(file_out, "w", encoding='utf-8') as f:
		json.dump(response, f, indent=4, ensure_ascii=False)

	print(f"Archivo guardado en '{file_out}'")

	#Aplicar los filtros a ese archivo
	if filters:
		results = {"Total":0,"Positivo":0,"Negativo":0,"Neutro":0,"questions":[]}
		qt = {}
		results.update(filters[0])

		for i in response:
			if all(i[name] == value for name, value in filters[0].items()):
				results["Total"] += 1
				results[i["clasification"]] += 1
				if not i[filters[1]["questions"]] in qt:qt[i[filters[1]["questions"]]]={"Total":0,"Positivo":0,"Negativo":0,"Neutro":0}
				qt[i[filters[1]["questions"]]][i["clasification"]]+=1
				qt[i[filters[1]["questions"]]]["Total"]+=1
		for i in qt:results["questions"].append({i:qt[i]})

		results["Positivo"] = str((results["Positivo"]/results["Total"])*100)[:4]+" %"
		results["Negativo"] = str((results["Negativo"]/results["Total"])*100)[:4]+" %"
		results["Neutro"] = str((results["Neutro"]/results["Total"])*100)[:4]+" %"

		with open(f"{ruta}/filters_output.json", "w", encoding='utf-8') as f:
			json.dump(results, f, indent=4, ensure_ascii=False)

		print("Resultados de los filtros guardados en:",(f"{ruta}/filters_output.json"))