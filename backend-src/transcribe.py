import requests
from time import sleep
import analyze_tone
import analyze_pace
from image_analysis import process_video

filler_file="filler_words.txt"
filler_words=set()
with open(filler_file, "r+") as f:	
	for line in f:
		filler_words.add(line.strip())

def process_audio(url, ID=None):
	response=audio_to_text(ID, url)
	output, tokens, colors, filler_freqs=get_text_and_fillers(response)
	tone_of_text=analyze_tone.process_text(output)
	pause_after_sent, pause_after_comma, words_per_min=analyze_pace.process_response(response)

	percentage_filler=sum(filler_freqs[freq] for freq in filler_freqs)/len(tokens)
	users_stats=[pause_after_sent, pause_after_comma, words_per_min, percentage_filler, filler_freqs, tone_of_text]
	ideal_stats=[2, 1, 150, 0, None, None]

	smile, datasets=process_video(url)

	data={}
	for tone in datasets:
		new_set=[]
		for point in datasets[tone]:
			new_set.append({"x":point[0], "y": point[1]})
		data[tone]=new_set

	return ((tokens, colors), (users_stats, ideal_stats), (data, smile))

def audio_to_text(ID, media_url):
	'''
	This function generates a dictionary representation of text from an audio file using the REV API. 
	'''
	new_headers= {
	   	'Authorization': 'Bearer 01wXudOy88gdkI2HgWeZUrc1WEp5GtFA5XK9KFNv6O7ucF6e5Nwe47CXm3cAbMAFHML56xeOQy0Ya99FFVwF7dqrzitwc',
	   	'Accept': 'application/vnd.rev.transcript.v1.0+json',
	}

	if ID==None:
		headers = {
		    'Authorization': 'Bearer 01wXudOy88gdkI2HgWeZUrc1WEp5GtFA5XK9KFNv6O7ucF6e5Nwe47CXm3cAbMAFHML56xeOQy0Ya99FFVwF7dqrzitwc'
		}

		url = "https://api.rev.ai/revspeech/v1beta/jobs"
		payload = {'media_url': media_url,
			'metadata': "Test"}
		response = requests.post(url, headers=headers, json=payload)

		response=response.json()
		ID=response["id"]

		status=response["status"]
		while status!='transcribed':
			sleep(30)
			response = requests.get('https://api.rev.ai/revspeech/v1beta/jobs/'+str(ID), headers=new_headers).json()
			status=response["status"]

	response2 = requests.get('https://api.rev.ai/revspeech/v1beta/jobs/'+str(ID)+'/transcript', headers=new_headers).json()

	return response2

def get_text_and_fillers(response2):
	colors={"blue": set()}
	filler_freqs={}
	text_portions=[]
	output=""
	parts=response2["monologues"][0]["elements"]

	for ind in range(len(parts)):
		elem=parts[ind]
		text_portions.append(elem["value"])
		output+=elem["value"]

		word=elem["value"].lower()
		if word in filler_words:
			if word not in filler_freqs:
				filler_freqs[word]=0
			filler_freqs[word]+=1
			colors["blue"].add(ind)

	return output, text_portions, colors, filler_freqs


url = "https://support.rev.com/hc/en-us/article_attachments/200043975/FTC_Sample_1_-_Single.mp3"
print("OUTPUT:", "\n", "\n", "\n", str(process_audio(url)))